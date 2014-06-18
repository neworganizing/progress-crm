import re
from django.db import IntegrityError
from actionkit import ActionKit
from progress_crm.adapters.base_adapter import BaseAdapter
from progress_crm.models import (Person, EmailAddress, PersonEmailAddress,
								 PostalAddress, PersonPostalAddress, List)

class ActionkitAdapter(BaseAdapter):
	errors = []

	def connect(self, url, username, password):
		self.connection = ActionKit(
			instance=url, username=username, password=password
		)
		print self.connection

	def sync(self, options={}):

		models_to_sync = options.get(
			'models',
			['person', 'list']
		)

		if 'person' in models_to_sync:
			self.sync_people(
				start_at=options.get('people_startat', 0),
				batch_size=options.get('people_batchsize', 100)
			)

		if 'list' in models_to_sync:
			self.sync_lists(
				batch_size = options.get('list_batchsize', 100)
			)

	def sync_lists(self, batch_size=100):
		lists = self.connection.list.list()

		for list_data in lists['objects']:
			self.sync_list(list_data, batch_size=batch_size)

	def sync_list(self, list_data, batch_size=100):
		list_object, created = List.objects.get_or_create(identifier=u'actionkit:{0}'.format(list_data['id']))
		list_object.name = list_data['name']
		list_object.type = 'email'
		list_object.is_dynamic = False
		list_object.save()

		subscription_count = self.connection.subscription.count(list=list_data['id'])
		index = 0
		list_complete = True

		while index < subscription_count:
			subscriptions = self.connection.subscription.list(
			 	list=list_data['id'],
			 	_offset=index,
			 	_limit=batch_size
			)

			for sub in subscriptions['objects']:
				try:				
					person = Person.objects.get(identifiers__contains=u'actionkit:{0}'.format(sub['user_id']))
				except Person.DoesNotExist:
					list_complete = False
					self.errors.append('User with actionkit id of {0} not found.'.format(sub['id']))

				item = ListItem(
					content_object=person,
					created_at=sub['created_at'],
					updated_at=sub['updated_at']
				)
				item.save()
				list_object.items.add(item)


	def sync_people(self, start_at=0, batch_size=100):
		people_count = self.connection.user.count()
		index = start_at

		while index < people_count:
			people = self.connection.user.list(_offset=index, _limit=batch_size)

			for person in people['objects']:
				self.sync_person(person)

			index += batch_size
			print "Imported {0} records...".format(index)

	def sync_person(self, person_data):
		"""
		Retreives a person's data, dedupes, and adds/updates as needed.
		"""

		print u"Syncing {0} {1}, {2}".format(person_data['first_name'], person_data['last_name'], person_data['id'])

		### Step 1: See if person exists by actionkit id
		matched = False
		try:
			# NOTE: Trailing comma is needed to distinguish actionkit:1 from actionkit:10, etc.
			matched_person = Person.objects.get(identifiers__contains=u'actionkit:{0},'.format(person_data['id']))
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
			person.add_identifier(u'actionkit:{0}'.format(person_data['id']))
		else:
			# If not matched, create a new person
			person = Person(**person_data_fields)
			# Set identifiers to Actionkit ID
			# NOTE: trailing comma is required for matching properly
			person.identifiers=u'actionkit:{0},'.format(person_data['id'])
			person.source=u'actionkit'

		person.save()

		# Create a new email address, or get existing one if already
		# in the database
		email_address, email_created = EmailAddress.objects.get_or_create(
			address=person_data['email'],
			address_type=u'personal'
		)
		email_address.save()

		person_data['address1'] = re.sub(r'[\"\'\,\:\\\r\n]', "", person_data['address1'])
		person_data['address1'] = person_data['address1'].encode('ascii', 'ignore')

		address_json = u'{"street_address": "'+person_data['address1']+'"}'

		try:
			json.loads(address_json)
		except:
			address_json = None

		# Ditto with postal address
		postal_address, postal_addr_created = PostalAddress.objects.get_or_create(
			status=u'verified',
			locality=person_data['city'],
			country=u'US',
			region=person_data['state'],
			postal_code=person_data['zip'],
			address_line=address_json,
			address_type=u'home'
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