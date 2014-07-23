from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from forms import SQLQueryForm

class SQLQueryView(FormView):
	template_name = "progress_crm_reporting/sql_query_form.html"
	form_class = SQLQueryForm

	def get_initial(self):
		if self.request.GET.get('new', False):
			if 'sql_data' in self.request.session:
				del self.request.session['sql_data']
			if 'sql_result' in self.request.session:
				del self.request.session['sql_result']
		else:
			sql_data = self.request.session.get('sql_data', None)
			if sql_data:
				self.initial = sql_data

		return super(SQLQueryView, self).get_initial()

	def form_valid(self, form):
		self.request.session['sql_data'] = form.cleaned_data
		self.request.session['sql_result'] = form.result()
		return super(SQLQueryView, self).form_valid(form)

	def get_success_url(self):
		print "Getting success URL!"
		print reverse('sql_query_result')
		return reverse('sql_query_result')

class SQLResultView(TemplateView):
	template_name = "progress_crm_reporting/sql_query_result.html"

	def get_context_data(self, **kwargs):
		context = super(SQLResultView, self).get_context_data(**kwargs)

		try:
			context['query_result'] = self.request.session['sql_result']
		except KeyError:
			messages.error('No SQL query result found, please write one here.')
			return HttpResponseRedirect(reverse('sql_query_form'))

		return context
