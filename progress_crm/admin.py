from django.contrib import admin
from .models import Person, Event, PostalAddress, Donation, FundraisingPage
from admin_tools.dashboard import registry

class PersonAdmin(admin.ModelAdmin):
	fieldsets = (
		('Name', {
			'fields': (('given_name', 'family_name', 'additional_name'), ('honorific_prefix', 'honorific_suffix'),)
		}),
		('Identity', {
			'fields': (('gender', 'gender_identity', 'party_identification'), ('source', 'identifiers'))
		}),
		('Birthdate', {
			'fields': (('birthdate_day', 'birthdate_month', 'birthdate_year'),)
		}),
		('Language', {
			'fields': ('ethnilocality', 'languages_spoken')
		}),
		('Employment', {
			'fields': ('employer', 'occupation')
		})
	)

	list_display = ('name', 'source', 'primary_email')

class EventAdmin(admin.ModelAdmin):
	fieldsets = (
		('General Info', {
			'fields': (('summary', 'identifier', 'status'), ('description', 'creator', 'organizer'))
		}),
		('Logistics', {
			'fields': (('location', 'start', 'end', 'all_day', 'all_day_date'), ('capacity', 'guests_allowed'), ('transparence', 'visibility'))
		}),
		('Reminders', {
			'fields': (('reminders', 'method', 'minutes'))
		})
	)

admin.site.register(Person, PersonAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(PostalAddress)
admin.site.register(Donation)
admin.site.register(FundraisingPage)