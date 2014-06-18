from admin_tools.dashboard.dashboards import AppIndexDashboard
from admin_tools.dashboard import modules
from django.utils.translation import ugettext_lazy as _

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
    The default dashboard displayed on the applications index page.
    To change the default dashboard you'll have to type the following from the
    commandline in your project root directory::

        python manage.py customdashboard

    And then set the ``ADMIN_TOOLS_APP_INDEX_DASHBOARD`` settings variable to
    point to your custom app index dashboard class.
    """

    # we disable title because its redundant with the model list module
    title = None

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module

        # TODO: Pull in models from plugins
        control_panel_modules = []

        for classname, module in CRMDashboardRegister.REGISTRY.iteritems():
            control_panel_modules.append(module())

        control_panel_modules.append(modules.ModelList('Database',self.models))

        self.children += [
            modules.Group(
                title="Control Panel",
                display="tabs",
                children=control_panel_modules
            ),
            CRMFundraisingModule('Fundraising Pages'),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]