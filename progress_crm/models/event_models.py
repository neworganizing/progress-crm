import datetime

from django.db import models
from django.core.exceptions import ValidationError
from jsonfield import JSONField

EVENT_STATUS_CHOICES = (
    ('confirmed', 'Confirmed'),
    ('tentative', 'Tentative'),
    ('cancelled', 'Cancelled')
)

TRANSPARENCE_CHOICES = (
    ('opaque', 'Opaque'),
    ('transparent', 'Transparent')
)

VISIBILITY_CHOICES = (
    ('public', 'Public'),
    ('private', 'Private')
)

METHOD_CHOICES = (
    ('email', 'Email'),
    ('sms', 'SMS')
)

class Event(models.Model):
    identifier = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=EVENT_STATUS_CHOICES, default='tentative')
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    summary = models.CharField(max_length=1023)
    description = models.TextField(blank=True)
    location = models.ForeignKey('PostalAddress')
    creator = models.ForeignKey('Person', related_name="created_events")
    organizer = models.ForeignKey('Person', related_name="organized_events", blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    all_day_date = models.DateField(blank=True, null=True)
    all_day = models.BooleanField(default=False)
    #recurrance = TBD
    transparence = models.CharField(max_length=255, choices=TRANSPARENCE_CHOICES, default='opaque')
    visibility = models.CharField(max_length=255, choices=VISIBILITY_CHOICES, default='public')
    # attendees = one to many with Attendees
    guests_allowed = models.BooleanField(default=False)
    reminders = JSONField(blank=True, null=True)
    method = models.CharField(max_length=127, choices=METHOD_CHOICES, blank=True, null=True)
    minutes = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    _total_accepted = None

    class Meta:
        app_label = 'progress_crm'

    @property
    def total_accepted(self):
        if not self._total_accepted:
            self._total_accepted = self.attendees.filter(status='accepted').count()
        return self._total_accepted

    def __unicode__(self):
        return self.summary

    def save(self):
        if not self.pk and not self.created:
            self.created = datetime.datetime.now()

        # Set updated field unless a new record with an existing updated field
        if not (not self.pk and self.updated):
            self.updated = datetime.datetime.now()

        return super(Event, self).save()


ATTENDANCE_STATUS_CHOCIES = (
    ('declined', 'Declined'),
    ('tentative', 'Tentative'),
    ('accepted', 'Accepted'),
    ('needs_action', 'Needs Action')
)

class Attendance(models.Model):
    identifier = models.CharField(max_length=255)
    event = models.ForeignKey(Event)
    person = models.ForeignKey('Person', related_name="events_attended")
    status = models.CharField(max_length=127, choices=ATTENDANCE_STATUS_CHOCIES, default='tentative')
    attended = models.NullBooleanField()
    comment = models.TextField()
    invited_by = models.ForeignKey('Person', related_name="guests_invited")

    class Meta:
        app_label = "progress_crm"
