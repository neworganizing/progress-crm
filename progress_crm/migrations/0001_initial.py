# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'progress_crm_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('family_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('given_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('additional_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('honorific_prefix', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('honorific_suffix', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=7, null=True, blank=True)),
            ('gender_identity', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('party_identification', self.gf('django.db.models.fields.CharField')(max_length=127, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('birthdate', self.gf('jsonfield.fields.JSONField')(max_length=128, null=True, blank=True)),
            ('birthdate_month', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('birthdate_day', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('birthdate_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ethnilocality', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('languages_spoken', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('employer', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('identifiers', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['Person'])

        # Adding model 'PostalAddress'
        db.create_table(u'progress_crm_postaladdress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_line', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
            ('locality', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=63, null=True, blank=True)),
            ('location', self.gf('jsonfield.fields.JSONField')(max_length=255, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('accuracy', self.gf('django.db.models.fields.CharField')(max_length=31, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['PostalAddress'])

        # Adding model 'PersonPostalAddress'
        db.create_table(u'progress_crm_personpostaladdress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.Person'])),
            ('postal_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.PostalAddress'])),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['PersonPostalAddress'])

        # Adding unique constraint on 'PersonPostalAddress', fields ['person', 'postal_address']
        db.create_unique(u'progress_crm_personpostaladdress', ['person_id', 'postal_address_id'])

        # Adding model 'EmailAddress'
        db.create_table(u'progress_crm_emailaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('address_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('progress_crm', ['EmailAddress'])

        # Adding model 'PersonEmailAddress'
        db.create_table(u'progress_crm_personemailaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.Person'])),
            ('email_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.EmailAddress'])),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['PersonEmailAddress'])

        # Adding unique constraint on 'PersonEmailAddress', fields ['person', 'email_address']
        db.create_unique(u'progress_crm_personemailaddress', ['person_id', 'email_address_id'])

        # Adding model 'PhoneNumber'
        db.create_table(u'progress_crm_phonenumber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('number_type', self.gf('django.db.models.fields.CharField')(max_length=31, null=True, blank=True)),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=63, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('sms_capable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('do_not_call', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['PhoneNumber'])

        # Adding unique constraint on 'PhoneNumber', fields ['number', 'extension']
        db.create_unique(u'progress_crm_phonenumber', ['number', 'extension'])

        # Adding model 'PersonPhoneNumber'
        db.create_table(u'progress_crm_personphonenumber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.Person'])),
            ('phone_number', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.PhoneNumber'])),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['PersonPhoneNumber'])

        # Adding unique constraint on 'PersonPhoneNumber', fields ['person', 'phone_number']
        db.create_unique(u'progress_crm_personphonenumber', ['person_id', 'phone_number_id'])

        # Adding model 'Profile'
        db.create_table(u'progress_crm_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profiles', to=orm['progress_crm.Person'])),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['Profile'])

        # Adding unique constraint on 'Profile', fields ['person', 'provider', 'identifier']
        db.create_unique(u'progress_crm_profile', ['person_id', 'provider', 'identifier'])

        # Adding model 'Event'
        db.create_table(u'progress_crm_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(default='tentative', max_length=255)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.PostalAddress'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_events', to=orm['progress_crm.Person'])),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='organized_events', null=True, to=orm['progress_crm.Person'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('all_day_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('all_day', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transparence', self.gf('django.db.models.fields.CharField')(default='opaque', max_length=255)),
            ('visibility', self.gf('django.db.models.fields.CharField')(default='public', max_length=255)),
            ('guests_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reminders', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=127, null=True, blank=True)),
            ('minutes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['Event'])

        # Adding model 'Attendance'
        db.create_table(u'progress_crm_attendance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.Event'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events_attended', to=orm['progress_crm.Person'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='tentative', max_length=127)),
            ('attended', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('invited_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='guests_invited', to=orm['progress_crm.Person'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['Attendance'])

        # Adding model 'Recipient'
        db.create_table(u'progress_crm_recipient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('legal_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('donation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipients', to=orm['progress_crm.Donation'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['Recipient'])

        # Adding model 'FundraisingPage'
        db.create_table(u'progress_crm_fundraisingpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifiers', self.gf('django.db.models.fields.TextField')()),
            ('originating_system', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.Person'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['FundraisingPage'])

        # Adding model 'Donation'
        db.create_table(u'progress_crm_donation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifiers', self.gf('django.db.models.fields.TextField')()),
            ('originating_system', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('donor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.Person'])),
            ('donated_at', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('credited_amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=2, blank=True)),
            ('credited_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('payment', self.gf('jsonfield.fields.JSONField')(default={})),
            ('subscription_instance', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('voided', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('voided_at', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('sources', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attributions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fundraising_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.FundraisingPage'], null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['Donation'])

        # Adding model 'List'
        db.create_table(u'progress_crm_list', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('is_dynamic', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['List'])

        # Adding model 'ListItem'
        db.create_table(u'progress_crm_listitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['progress_crm.List'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('progress_crm', ['ListItem'])

        # Adding unique constraint on 'ListItem', fields ['list', 'content_type', 'object_id']
        db.create_unique(u'progress_crm_listitem', ['list_id', 'content_type_id', 'object_id'])

        # Adding model 'Form'
        db.create_table(u'progress_crm_form', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifiers', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('call_to_action', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['progress_crm.Person'], null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('progress_crm', ['Form'])

        # Adding model 'Submission'
        db.create_table(u'progress_crm_submission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifiers', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='form_submissions', to=orm['progress_crm.Person'])),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='submissions', to=orm['progress_crm.Form'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('progress_crm', ['Submission'])


    def backwards(self, orm):
        # Removing unique constraint on 'ListItem', fields ['list', 'content_type', 'object_id']
        db.delete_unique(u'progress_crm_listitem', ['list_id', 'content_type_id', 'object_id'])

        # Removing unique constraint on 'Profile', fields ['person', 'provider', 'identifier']
        db.delete_unique(u'progress_crm_profile', ['person_id', 'provider', 'identifier'])

        # Removing unique constraint on 'PersonPhoneNumber', fields ['person', 'phone_number']
        db.delete_unique(u'progress_crm_personphonenumber', ['person_id', 'phone_number_id'])

        # Removing unique constraint on 'PhoneNumber', fields ['number', 'extension']
        db.delete_unique(u'progress_crm_phonenumber', ['number', 'extension'])

        # Removing unique constraint on 'PersonEmailAddress', fields ['person', 'email_address']
        db.delete_unique(u'progress_crm_personemailaddress', ['person_id', 'email_address_id'])

        # Removing unique constraint on 'PersonPostalAddress', fields ['person', 'postal_address']
        db.delete_unique(u'progress_crm_personpostaladdress', ['person_id', 'postal_address_id'])

        # Deleting model 'Person'
        db.delete_table(u'progress_crm_person')

        # Deleting model 'PostalAddress'
        db.delete_table(u'progress_crm_postaladdress')

        # Deleting model 'PersonPostalAddress'
        db.delete_table(u'progress_crm_personpostaladdress')

        # Deleting model 'EmailAddress'
        db.delete_table(u'progress_crm_emailaddress')

        # Deleting model 'PersonEmailAddress'
        db.delete_table(u'progress_crm_personemailaddress')

        # Deleting model 'PhoneNumber'
        db.delete_table(u'progress_crm_phonenumber')

        # Deleting model 'PersonPhoneNumber'
        db.delete_table(u'progress_crm_personphonenumber')

        # Deleting model 'Profile'
        db.delete_table(u'progress_crm_profile')

        # Deleting model 'Event'
        db.delete_table(u'progress_crm_event')

        # Deleting model 'Attendance'
        db.delete_table(u'progress_crm_attendance')

        # Deleting model 'Recipient'
        db.delete_table(u'progress_crm_recipient')

        # Deleting model 'FundraisingPage'
        db.delete_table(u'progress_crm_fundraisingpage')

        # Deleting model 'Donation'
        db.delete_table(u'progress_crm_donation')

        # Deleting model 'List'
        db.delete_table(u'progress_crm_list')

        # Deleting model 'ListItem'
        db.delete_table(u'progress_crm_listitem')

        # Deleting model 'Form'
        db.delete_table(u'progress_crm_form')

        # Deleting model 'Submission'
        db.delete_table(u'progress_crm_submission')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'progress_crm.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'attended': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'invited_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'guests_invited'", 'to': "orm['progress_crm.Person']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events_attended'", 'to': "orm['progress_crm.Person']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'tentative'", 'max_length': '127'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.donation': {
            'Meta': {'object_name': 'Donation'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'attributions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'credited_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '2', 'blank': 'True'}),
            'credited_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'donated_at': ('django.db.models.fields.DateField', [], {}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.Person']"}),
            'fundraising_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.FundraisingPage']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifiers': ('django.db.models.fields.TextField', [], {}),
            'originating_system': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'payment': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subscription_instance': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'voided': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'voided_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.emailaddress': {
            'Meta': {'object_name': 'EmailAddress'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'address_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'progress_crm.event': {
            'Meta': {'object_name': 'Event'},
            'all_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'all_day_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_events'", 'to': "orm['progress_crm.Person']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'guests_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.PostalAddress']"}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organized_events'", 'null': 'True', 'to': "orm['progress_crm.Person']"}),
            'reminders': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'tentative'", 'max_length': '255'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'transparence': ('django.db.models.fields.CharField', [], {'default': "'opaque'", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'visibility': ('django.db.models.fields.CharField', [], {'default': "'public'", 'max_length': '255'})
        },
        'progress_crm.form': {
            'Meta': {'object_name': 'Form'},
            'call_to_action': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.Person']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifiers': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'progress_crm.fundraisingpage': {
            'Meta': {'object_name': 'FundraisingPage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.Person']"}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifiers': ('django.db.models.fields.TextField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'originating_system': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'progress_crm.list': {
            'Meta': {'object_name': 'List'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'is_dynamic': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.listitem': {
            'Meta': {'unique_together': "(['list', 'content_type', 'object_id'],)", 'object_name': 'ListItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['progress_crm.List']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.person': {
            'Meta': {'object_name': 'Person'},
            'additional_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'birthdate': ('jsonfield.fields.JSONField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'birthdate_day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_addresses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['progress_crm.EmailAddress']", 'through': "orm['progress_crm.PersonEmailAddress']", 'symmetrical': 'False'}),
            'employer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ethnilocality': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'gender_identity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'honorific_prefix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'honorific_suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifiers': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'languages_spoken': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'party_identification': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'phone_numbers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['progress_crm.PhoneNumber']", 'through': "orm['progress_crm.PersonPhoneNumber']", 'symmetrical': 'False'}),
            'postal_addresses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['progress_crm.PostalAddress']", 'through': "orm['progress_crm.PersonPostalAddress']", 'symmetrical': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.personemailaddress': {
            'Meta': {'unique_together': "(['person', 'email_address'],)", 'object_name': 'PersonEmailAddress'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.EmailAddress']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.Person']"}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.personphonenumber': {
            'Meta': {'unique_together': "(['person', 'phone_number'],)", 'object_name': 'PersonPhoneNumber'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.Person']"}),
            'phone_number': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.PhoneNumber']"}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.personpostaladdress': {
            'Meta': {'unique_together': "(['person', 'postal_address'],)", 'object_name': 'PersonPostalAddress'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.Person']"}),
            'postal_address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['progress_crm.PostalAddress']"}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.phonenumber': {
            'Meta': {'unique_together': "(('number', 'extension'),)", 'object_name': 'PhoneNumber'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'do_not_call': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'number_type': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'sms_capable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.postaladdress': {
            'Meta': {'object_name': 'PostalAddress'},
            'accuracy': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            'address_line': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'address_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'location': ('jsonfield.fields.JSONField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.profile': {
            'Meta': {'unique_together': "(['person', 'provider', 'identifier'],)", 'object_name': 'Profile'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profiles'", 'to': "orm['progress_crm.Person']"}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'progress_crm.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'donation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipients'", 'to': "orm['progress_crm.Donation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legal_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'progress_crm.submission': {
            'Meta': {'object_name': 'Submission'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'to': "orm['progress_crm.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifiers': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'form_submissions'", 'to': "orm['progress_crm.Person']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['progress_crm']