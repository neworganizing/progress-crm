from django.db import models
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class List(models.Model):
	'''
	A list that is capable of holding items of any type.

	identifier		string	A internally unique identifier, usually URL friendly
	name 			string	Name of list
	description		string	A description of a list, eg "2012 donors"
	type			string	A string description of the type of resources, eg "events"
	is_dynamic		bool	A boolean value that indicates if the list is static or dynamic
	'''
	identifier = models.CharField(max_length=1023)
	name = models.CharField(max_length=1023)
	description = models.TextField(blank=True, null=True)
	type = models.CharField(max_length=127)
	is_dynamic = models.NullBooleanField()

	created_at = models.DateTimeField(null=True, blank=True)
	updated_at = models.DateTimeField(null=True, blank=True)
	#items = reverse relation

	class Meta:
		app_label = 'progress_crm'

	def __unicode__(self):
		return self.name

	def item_count(self):
		return self.items.count()

class ListItem(models.Model):
	'''
	We use Django's GenericRelation to create a list model that can hold any
	other type of model.
	'''
	list = models.ForeignKey(List, related_name='items')
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	
	created_at = models.DateTimeField(null=True, blank=True)
	updated_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		app_label = 'progress_crm'
		unique_together = ['list', 'content_type', 'object_id']

	def __unicode__(self):
		return u"List item {0} - {1}".format(content_type, object_id)