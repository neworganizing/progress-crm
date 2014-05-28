from django.test import TestCase

from ..models import *

class PersonTests(TestCase):
	def test_create_person(self):
		'''
		Tests creating a basic person
		'''
		person = Person()
		person.save()
		self.assertEqual(Person.objects.count(), 1)

	def test_invalid_phone_number(self):
		'''
		Ensures that a phone number object cannot be
		created without an actual number.
		'''
		phone_number = PhoneNumber()

		with self.assertRaises(ValidationError):
			phone_number.full_clean()
			phone_number.save()

		self.assertEqual(PhoneNumber.objects.count(), 0)

	def test_invalid_email_address(self):
		'''
		Ensures that an email address object cannot be
		created without an actual email.
		'''
		email_address = EmailAddress()

		with self.assertRaises(ValidationError):
			email_address.full_clean()
			email_address.save()

		self.assertEqual(EmailAddress.objects.count(), 0)

	def test_invalid_postal_address(self):
		'''
		Ensures that a postal address object cannot be
		created without an actual address.
		'''
		postal_address = PostalAddress()

		with self.assertRaises(ValidationError):
			postal_address.full_clean()
			postal_address.save()

		self.assertEqual(EmailAddress.objects.count(), 0)

	def test_invalid_profiles(self):
		'''
		Test that a blank profile throws validation errors
		'''
		profile = Profile()

		with self.assertRaises(ValidationError):
			profile.full_clean()
			profile.save()

		self.assertEqual(Profile.objects.count(), 0)

	def test_create_person_with_relations(self):
		'''
		Tests creating a person with related objects and only required fields.
		'''
		email_address = EmailAddress(address='tester@test.com', address_type='personal')
		email_address.full_clean()
		email_address.save()

		postal_address = PostalAddress(
			status='verified',
			locality='Washington',
			country='US',
			region='DC',
			postal_code='20036',
			address_line='{"street_address": "1133 19th Street NW"}',
			address_type='work'
		)
		postal_address.full_clean()
		postal_address.save()

		phone_number = PhoneNumber(
				country="US",
				number="202-555-1234"
		)
		phone_number.full_clean()
		phone_number.save()

		person = Person(
				source='user_created'
		)
		person.full_clean()
		person.save()

		person_email_address = PersonEmailAddress(person=person, email_address=email_address)
		person_email_address.save()

		person_postal_address = PersonPostalAddress(person=person, postal_address=postal_address)
		person_postal_address.save()

		person_phone_number = PersonPhoneNumber(person=person, phone_number=phone_number)
		person_phone_number.save()

		profile = Profile(
			person=person,
			identifier='123456789',
			handle='myhandle',
			provider='friendster',
			url='http://www.friendster.com/'
		)

		profile.full_clean()
		profile.save()

		person.save()

		self.assertEqual(Person.objects.count(), 1)
		self.assertEqual(person.email_addresses.count(), 1)
		self.assertEqual(person.postal_addresses.count(), 1)
		self.assertEqual(person.phone_numbers.count(), 1)
		self.assertEqual(person.profiles.count(), 1)