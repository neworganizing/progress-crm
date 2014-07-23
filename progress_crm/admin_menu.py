from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

try:
	from admin_tools.menu import items
	from admin_tools.utils import get_admin_site_name
	from admin_tools.menu.menus import Menu
except ImportError:
	raise ImproperlyConfigured("Django-Admin-Tools must be installed to use this feature")

class CRMMenu(Menu):
	"""
	Override default menu to setup for ProgressCRM
	"""
	def init_with_context(self, context):
		site_name = get_admin_site_name(context)

		self.children += [
			items.MenuItem(_('Dashboard'), reverse('%s:index' % site_name)),
			items.MenuItem(_('ProgressCRM'), '/admin/progress_crm/'),
			items.AppList(
				_('Applications'),
				exclude=('django.contrib.*', 'progress_crm*')
			),
			items.AppList(
				_('Administration'),
				models=('django.contrib.*',)
			)
		]