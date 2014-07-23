from django import forms
from django.db import connection

class SQLQueryForm(forms.Form):
	name = forms.CharField()
	script = forms.CharField(widget=forms.Textarea())

	def result(self):
		cursor = connection.cursor()
		cursor.execute(self.cleaned_data['script'])
		result = cursor.fetchall()
		return result