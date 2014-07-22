import re
import pytz
from dateutil.parser import parse
from django.db import IntegrityError
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from actionkit import ActionKit
from progress_crm.adapters.base_adapter import BaseAdapter
from progress_crm.models import (Person, EmailAddress, PersonEmailAddress,
								 PostalAddress, PersonPostalAddress, List,
								 ListItem, Donation, Form, Submission)

class ActionkitAdapter(BaseAdapter):
	"""
	An adapter wrapping python-actionkit, which is a library for interacting with the ActionKit API.
	"""
	adapter_name = 'Actionkit'
	max_batchsize = 100
	person_type = None

	def __init__(self, *args, **kwargs):
		self.person_type = ContentType.objects.get(app_label="progress_crm", model="person")
		return super(ActionkitAdapter, self).__init__(*args, **kwargs)

	def connect(self, url, username, password):
		self.connection = ActionKit(
			instance=url, username=username, password=password
		)

	def get_people_count(self):
		return self.connection.user.count()

	def get_people(self, index, batch_size):
		return self.connection.user.list(_offset=index, _limit=batch_size)['objects']

	def create_person(self, person_data):
		"""
		Retreives a person's data, dedupes, and adds/updates as needed.
		"""

		#print u"Syncing {0} {1}, {2}".format(person_data['first_name'], person_data['last_name'], person_data['id'])

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
			address=person_data['email'], address_type=u'personal'
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
			status=u'verified', locality=person_data['city'],
			country=u'US', region=person_data['state'],	postal_code=person_data['zip'],
			address_line=address_json, address_type=u'home'
		)
		postal_address.save()

		# Attempt to assign email and postal address to the person,
		# ignoring if they have already been assigned

		# TODO: Add flags for controlling what is set to primary and when
		person_email_address, pea_created = PersonEmailAddress.objects.get_or_create(
			person=person, email_address=email_address
		)
		person_email_address.primary = True
		person_email_address.save()

		person_postal_address, ppa_created = PersonPostalAddress.objects.get_or_create(
			person=person, postal_address=postal_address
		)
		person_postal_address.primary = True
		person_postal_address.save()

	def get_lists(self):
		return self.connection.list.list()['objects']

	def get_list_item_count(self, list_data):
		return self.connection.subscription.count(list=list_data['id'])

	def get_list_items(self, list_data, index, batch_size):
		return self.connection.subscription.list(
		 	list=list_data['id'],
		 	_offset=index,
		 	_limit=batch_size
		)['objects']

	def get_donations_count(self):
		return self.connection.donationaction.count()

	def get_donations(self, index, batch_size):
		donations = self.connection.order.list(_offset=index, _limit=batch_size)['objects']
		return donations

	def get_forms_count(self):
		return self.connection.page.count()

	def get_forms(self, index, batch_size):
		return self.connection.page.list(_offset=index, _limit=batch_size)['objects']

	def get_form_submissions_count(self):
		return self.connection.action.count()

	def get_form_submissions(self, index, batch_size):
		return self.connection.action.list(_offset=index, _limit=batch_size)['objects']

	def create_list(self, list_data):
		list_object, created = List.objects.get_or_create(identifier=u'actionkit:{0}'.format(list_data['id']))
		list_object.name = list_data['name']
		list_object.type = 'email'
		list_object.is_dynamic = False
		list_object.save()
		return list_object

	def create_form(self, form_data):
		created = False
		try:
			form = Form.objects.get(identifiers__contains=u'actionkit:{0},'.format(form_data['id']))
			created = True
		except Form.DoesNotExist:
			form = Form(identifiers=u'actionkit:{0},'.format(form_data['id']))

		form.created_at = pytz.utc.localize(parse(form_data['created_at']))
		form.updated_at = pytz.utc.localize(parse(form_data['updated_at']))
		form.name = form_data['name']
		form.title = form_data['title']
		form.summary = ''
		form.description = ''
		form.call_to_action = ''
		form.url = form_data['resource_uri']

		form.save()

	def create_form_submission(self, form_submission_data):
		created = False
		try:
			submission = Submission.objects.get(identifiers__contains=u'actionkit:{0},'.format(form_submission_data['id']))
			created = True
		except Submission.DoesNotExist:
			submission = Submission(identifiers=u'actionkit:{0},'.format(form_submission_data['id']))

		submission.created_at = pytz.utc.localize(parse(form_submission_data['created_at']))
		submission.updated_at = pytz.utc.localize(parse(form_submission_data['updated_at']))

		user_id = form_submission_data['user'].split('/')[-2]
		try:
			person = Person.objects.get(identifiers__contains=u'actionkit:{0},'.format(user_id))
		except Person.DoesNotExist:
			error_message = 'User with actionkit id of {0} not found.'.format(user_id)
			print error_message
			self.errors.append(error_message)
			return
			
		submission.person = person

		form_id = form_submission_data['page'].split('/')[-2]
		try:				
			form = Form.objects.get(identifiers__contains=u'actionkit:{0},'.format(form_id))
		except Form.DoesNotExist:
			error_message = 'User with actionkit id of {0} not found.'.format(form_id)
			print error_message
			self.errors.append(error_message)
			return

		submission.form = form
		submission.save()

	def create_donation(self, donation_data):
		created = False
		try:
			donation_object = Donation.objects.get(identifiers__contains=u'actionkit:{0},'.format(donation_data['id']))
			created = True
		except Donation.DoesNotExist:
			donation_object = Donation(identifiers=u'actionkit:{0},'.format(donation_data['id']))

		donation_object.created_at = pytz.utc.localize(parse(donation_data['created_at']))
		donation_object.updated_at = pytz.utc.localize(parse(donation_data['updated_at']))
		donation_object.originating_system = 'actionkit'

		user_id = donation_data['user'].split('/')[-2]
		try:				
			person = Person.objects.get(identifiers__contains=u'actionkit:{0},'.format(user_id))
		except Person.DoesNotExist:
			error_message = 'User with actionkit id of {0} not found.'.format(user_id)
			print error_message
			self.errors.append(error_message)
			return
			
		donation_object.donor = person
		donation_object.donated_at = donation_object.created_at
		donation_object.amount = donation_data['total']
		donation_object.currency = donation_data['currency']
		donation_object.url = donation_data['resource_uri']
		donation_object.save()

	def create_list_item(self, list_item_data, list_object):
		"""
		Actionkit only supports lists of users, so we can assume all
		objects are Person objects.
		"""
		user_id = list_item_data['user'].split('/')[-2]
		try:				
			person = Person.objects.get(identifiers__contains=u'actionkit:{0},'.format(user_id))
		except Person.DoesNotExist:
			error_message = 'User with actionkit id of {0} not found.'.format(user_id)
			print error_message
			self.errors.append(error_message)
			return

		created_at = pytz.utc.localize(parse(list_item_data['created_at']))
		updated_at = pytz.utc.localize(parse(list_item_data['updated_at']))

		item, li_created = ListItem.objects.get_or_create(
			list=list_object,
			content_type=self.person_type,
			object_id=person.pk
		)
		item.created_at=created_at
		item.updated_at=updated_at
		item.save()