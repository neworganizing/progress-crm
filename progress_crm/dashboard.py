from admin_tools.dashboard.dashboards import AppIndexDashboard
from admin_tools.dashboard import modules
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from progress_crm.models import FundraisingPage
from progress_crm.plugins import CRMDashboardRegister

class CRMFundraisingModule(modules.DashboardModule):
    def is_empty(self):
        return False

    def init_with_context(self, context):
        for page in FundraisingPage.objects.all():
            self.children.append(page)

class CRMDashboard(AppIndexDashboard):
    """
    ProgressCRM's custom dashboard system.
    """

    # we disable title because its redundant with the model list module
    title = None
    columns = 1

    class Media:
        css = None
        js = ('js/progress_crm.js',)

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module

        # TODO: Pull in models from plugins
        control_panel_modules = []

        if hasattr(settings, 'PCRM_DASHBOARD_ORDER'):
            for classname in settings.PCRM_DASHBOARD_ORDER:
                try:
                    module = CRMDashboardRegister.REGISTRY[classname]
                    print module
                    control_panel_modules.append(module())
                except KeyError:
                    raise ImproperlyConfigured("Class in PCRM_DASHBOARD_ORDER has not been registered.")
        else:
            for classname, module in CRMDashboardRegister.REGISTRY.iteritems():
                control_panel_modules.append(module())

        control_panel_modules.append(modules.ModelList('Database',self.models))

        self.children += [
            modules.Group(
                title="Control Panel",
                display="tabs",
                children=control_panel_modules
            )
        ]