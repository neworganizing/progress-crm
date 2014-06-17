import re
from actionkit import ActionKit
from progress_crm.adapters.base_adapter import BaseAdapter
from progress_crm.models import Person, EmailAddress, PersonEmailAddress, PostalAddress, PersonPostalAddress

class ActionkitAdapter(BaseAdapter):
	def connect(self, url, username, password):
		self.connection = ActionKit(
			instance=url, username=username, password=password
		)
		print self.connection

	def sync(self, models=[], batch_size=100):
		total_people = self.connection.user.count()
		current_count = 0

		while current_count < total_people:
			people = self.connection.user.list(_offset=current_count, _limit=batch_size)

			for person in people['objects']:
				self.sync_person(person)

			current_count += batch_size
			print "Imported {0} records...".format(current_count)

	def sync_person(self, person_data):
		"""
		Retreives a person's data, dedupes, and adds/updates as needed.
		"""

		print "Syncing {0} {1}, {2}".format(person_data['first_name'], person_data['last_name'], person_data['id'])

		### Step 1: See if person exists by actionkit id
		matched = False
		try:
			# NOTE: Trailing comma is needed to distinguish actionkit:1 from actionkit:10, etc.
			matched_person = Person.objects.get(identifiers__contains='actionkit:{0},'.format(person_data['id']))
			matched = True
		except Person.DoesNotExist:
			matched_person = None

		person_data_fields = dict(
			family_name=person_data['last_name'],
			given_name=person_data['first_name'],
			additional_name=person_data['middle_name'],
			languages_spoken=person_data['lang']
		)

		if matched:
			# If matched, update data
			person = matched_person

			for key, value in person_data_fields.iteritems():
				setattr(person, key, value)

			# add identifier, as other identifiers may already exist
			person.add_identifier('actionkit:{0}'.format(person_data['id']))
		else:
			# If not matched, create a new person
			person = Person(**person_data_fields)
			# Set identifiers to Actionkit ID
			# NOTE: trailing comma is required for matching properly
			person.identifiers='actionkit:{0},'.format(person_data['id'])
			person.source='actionkit'

		person.save()

		# Create a new email address, or get existing one if already
		# in the database
		email_address, email_created = EmailAddress.objects.get_or_create(
			address=person_data['email'],
			address_type='personal'
		)
		email_address.save()

		person_data['address1'] = re.sub(r"[\"\'\,]", "", person_data['address1'])

		# Ditto with postal address
		postal_address, postal_addr_created = PostalAddress.objects.get_or_create(
			status='verified',
			locality=person_data['city'],
			country='US',
			region=person_data['state'],
			postal_code=person_data['zip'],
			address_line='{"street_address": "'+person_data['address1']+'"}',
			address_type='home'
		)
		postal_address.save()

		# Attempt to assign email and postal address to the person,
		# ignoring if they have already been assigned

		try:
			person_email_address = PersonEmailAddress(person=person, email_address=email_address)
			if person.email_addresses.count() == 0:
				person_email_address.primary = True
			person_email_address.save()
		except IntegrityError:
			pass

		try:
			person_postal_address = PersonPostalAddress(person=person, postal_address=postal_address)
			if person.postal_addresses.count() == 0:
				person_postal_address.primary = True
			person_postal_address.save()
		except IntegrityError:
			pass