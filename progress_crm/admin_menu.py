from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

try:
	from admin_tools.menu import items
	from admin_tools.menu.menus import DefaultMenu
except ImportError:
	raise ImproperlyConfigured("Django-Admin-Tools must be installed to use this feature")

class CRMMenu(DefaultMenu):
	def init_with_context(self, context):
		super(CRMMenu, self).init_with_context(context)
		self.children.insert(2, items.MenuItem(_('ProgressCRM'), '/admin/progress_crm/'))