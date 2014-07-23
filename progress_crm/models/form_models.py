from django.db import models

class Form(models.Model):
	"""
	identifiers	Identifier[]	An array of identifiers the provider has determined to be associated with the form
	created_date	datetime	Date and Time of creation
	modified_date	datetime	Date and Time of last modification
	name	string	name of the form
	title	string	title of the form
	summary	string	summary of the form
	description	string/html string	description of the form, optionally an HTML string
	call_to_action	string	Text of the call to action of the form (ex: Fill out our survey)
	url	string	A URL string pointing to the publicly available form page on the web
	total_submissions	integer	Read-only computed property representing the current count of submissions on the form
	creator	Person*	A single embedded instance of a person representing the creator of the form
	submissions	Submissions[]*	A Collection of Submission resources
	"""
	identifiers = models.CharField(max_length=1024)
	name = models.CharField(max_length=512)
	title = models.CharField(max_length=512)
	summary = models.TextField()
	description = models.TextField()
	call_to_action = models.TextField()
	url = models.URLField()
	creator = models.ForeignKey('Person', null=True, blank=True)
	
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

	class Meta:
		app_label = "progress_crm"

	def total_submissions(self):
		"""
		Returns the total number of submissions to this form.
		"""
		pass

class Submission(models.Model):
	"""
	identifiers	Identifier[]	An array of identifiers the provider has determined to be associated with the form
	created_date	datetime	Date and Time of creation
	modified_date	datetime	Date and Time of last modification
	person	Person*	An embedded person that made the submission on the referenced form
	form	Form*	A reference to the form this submission is related to
	question_answers	Question_Answers[]*	A Collection of Question Answer resources related to this submission
	"""
	identifiers = models.CharField(max_length=1024)
	person = models.ForeignKey('Person', related_name="form_submissions")
	form = models.ForeignKey(Form, related_name="submissions")
	#question_answers

	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

	class Meta:
		app_label = "progress_crm"