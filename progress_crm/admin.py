from django.contrib import admin
from .models import Person
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

admin.site.register(Person, PersonAdmin)