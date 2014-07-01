from django.db import models

SYNC_CHOICES = (
	('Pending', 'pending'),
	('Running', 'running'),
	('Complete', 'complete'),
	('Error', 'error')
)

class SyncOperation(models.Model):
	sync_at = models.DateTimeField()
	type = models.CharField(max_length=255)
	current_record = models.IntegerField()
	total_records = models.IntegerField()
	errors = models.TextField()
	organization = models.ForeignKey('Organization', related_name='sync_ops')
	status = models.CharField(max_length=255, choices=SYNC_CHOICES)