from django.db import models
from django.core.exceptions import ValidationError
from jsonfield import JSONField

GENDER_CHOICES = (
	('female', 'Female'),
	('male', 'Male'),
	('other', 'Other')
)

PARTY_CHOICES = (
	('none', 'None'),
	('democrat', 'Democrat'),
	('republican', 'Republican'),
	('independent', 'Independent')
)

# Data model for a person based on OSDI
# spec, found here: https://github.com/opensupporter/osdi-docs/blob/master/people.md

class Person(models.Model):
	# Person id fields
	family_name = models.CharField(max_length=255, null=True, blank=True)
	given_name = models.CharField(max_length=255, null=True, blank=True)
	additional_name = models.CharField(max_length=255, null=True, blank=True)
	honorific_prefix = models.CharField(max_length=255, null=True, blank=True)
	honorific_suffix = models.CharField(max_length=255, null=True, blank=True)
	gender = models.CharField(max_length=7, choices=GENDER_CHOICES, null=True, blank=True)
	gender_identity = models.CharField(max_length=255, null=True, blank=True)
	party_identification = models.CharField(max_length=127, choices=PARTY_CHOICES, null=True, blank=True)
	
	# Source of this person's first instance
	source = models.CharField(max_length=255)
	
	birthdate = JSONField(max_length=128, null=True, blank=True)
	birthdate_month = models.IntegerField(null=True, blank=True)
	birthdate_day = models.IntegerField(null=True, blank=True)
	birthdate_year = models.IntegerField(null=True, blank=True)

	# Ethnographic data	
	ethnilocality = models.CharField(max_length=255, null=True, blank=True)
	languages_spoken = models.TextField(null=True, blank=True)

	# Employer data
	employer = models.CharField(max_length=255, null=True, blank=True)
	occupation = models.CharField(max_length=255, null=True, blank=True)

	# External identifiers
	identifiers = models.TextField(null=True, blank=True)

	postal_addresses = models.ManyToManyField('PostalAddress', through='PersonPostalAddress')
	email_addresses = models.ManyToManyField('EmailAddress', through='PersonEmailAddress')
	phone_numbers = models.ManyToManyField('PhoneNumber', through='PersonPhoneNumber')
	# profiles reverse relation to Profile model

	_primary_email = None

	class Meta:
		app_label = 'progress_crm'
		verbose_name_plural = 'people'

	def __unicode__(self):
		return u"{0}".format(self.name())

	def name(self):
		return "{0} {1}".format(self.given_name, self.family_name)

	def primary_email(self):
		if not self._primary_email:
			try:
				self._primary_email = self.personemailaddress_set.get(primary=True).email_address.address
			except PersonEmailAddress.DoesNotExist:
				self._primary_email = 'No email'
		return self._primary_email

	def add_identifier(self, identifier):
		id_array = self.identifiers.split(',')
		if identifier not in id_array:
			id_array.append(identifier)
			self.identifiers = ','.join(id_array)

POSTAL_ADDRESS_TYPES = (
	('home', 'Home'),
	('work', 'Work'),
	('mailing', 'Mailing'),
)

GEO_ACCURACY_CHOICES = (
	('rooftop', 'Rooftop'),
	('approximate', 'Approximate'),
)

POSTAL_ADDRESS_STATUS_CHOICES = (
	('potential', 'Potential'),
	('verified', 'Verified'),
	('bad', 'Bad'),
)

class PostalAddress(models.Model):
	address_type = models.CharField(max_length=255, choices=POSTAL_ADDRESS_TYPES)
	address_line = JSONField()
	locality = models.CharField(max_length=255)
	region = models.CharField(max_length=2)
	postal_code = models.CharField(max_length=63)
	country = models.CharField(max_length=2)
	language = models.CharField(max_length=63, null=True, blank=True)
	location = JSONField(max_length=255, null=True, blank=True)
	latitude = models.FloatField(null=True, blank=True)
	longitude = models.FloatField(null=True, blank=True)
	accuracy = models.CharField(max_length=31, choices=GEO_ACCURACY_CHOICES, blank=True, null=True)
	status = models.CharField(max_length=31, choices=POSTAL_ADDRESS_STATUS_CHOICES)

	class Meta:
		app_label = 'progress_crm'

	def __unicode__(self):
		return "{0}".format(self.address_line)

class PersonPostalAddress(models.Model):
	person = models.ForeignKey(Person)
	postal_address = models.ForeignKey(PostalAddress)
	primary = models.BooleanField(default=False)

	class Meta:
		app_label = 'progress_crm'
		unique_together = ['person', 'postal_address']

EMAIL_TYPE_CHOICES = (
	('personal', 'Personal'),
	('work', 'Work')
)

class EmailAddress(models.Model):
	address = models.CharField(max_length=254)
	address_type = models.CharField(max_length=255)

	class Meta:
		app_label = 'progress_crm'

	def __unicode__(self):
		return "{0} ({1})".format(self.address, self.address_type)

class PersonEmailAddress(models.Model):
	person = models.ForeignKey(Person)
	email_address = models.ForeignKey(EmailAddress)
	primary = models.BooleanField(default=False)

	class Meta:
		app_label = 'progress_crm'
		unique_together = ['person', 'email_address']

PHONE_TYPE_CHOICES = (
	('home', 'Home'),
	('work', 'Work'),
	('mobile', 'Mobile'),
	('other', 'Other'),
	('daytime', 'Daytime'),
	('evening', 'Evening'),
	('fax', 'Fax')
)

class PhoneNumber(models.Model):
	number = models.CharField(max_length=15)
	extension = models.CharField(max_length=4, null=True, blank=True)
	number_type = models.CharField(max_length=31, choices=PHONE_TYPE_CHOICES, null=True, blank=True)
	operator = models.CharField(max_length=63, blank=True, null=True)
	country = models.CharField(max_length=2)
	sms_capable = models.BooleanField(default=False)
	do_not_call = models.BooleanField(default=False)

	class Meta:
		app_label = 'progress_crm'
		unique_together = ('number', 'extension',)

	def clean(self):
		if self.number == '' or not self.number:
			raise ValidationError('A number must be provided.')

		self.number = self.number.replace(r'[^0-9]', '')

class PersonPhoneNumber(models.Model):
	person = models.ForeignKey(Person)
	phone_number = models.ForeignKey(PhoneNumber)
	primary = models.BooleanField(default=False)
	description = models.TextField()

	class Meta:
		app_label = 'progress_crm'
		unique_together = ['person', 'phone_number']

class Profile(models.Model):
	person = models.ForeignKey(Person, related_name='profiles')
	provider = models.CharField(max_length=63)
	identifier = models.CharField(max_length=255)
	url = models.URLField()
	handle = models.CharField(max_length=127)

	class Meta:
		app_label = 'progress_crm'
		unique_together = ['person', 'provider', 'identifier']

	def __unicode__(self):
		return u"{0}'s {1} profile".format(person.name(), provider)