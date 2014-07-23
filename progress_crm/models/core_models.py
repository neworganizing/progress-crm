from django.db import models

class Organization(models.Model):
	name = models.CharField(max_length=255)
	abbreviation = models.CharField(max_length=31)
	parent = models.ForeignKey('Organization', related_name='children')
	address = models.ForeignKey('PostalAddress')

	created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		app_label = 'progress_crm'

	def __unicode__(self):
		return self.name