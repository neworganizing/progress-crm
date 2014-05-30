from admin_tools.dashboard.dashboards import AppIndexDashboard
from admin_tools.dashboard import modules
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum

from progress_crm.models import Person, Event, Donation, FundraisingPage

class CRMFundraisingModule(modules.DashboardModule):
    def init_with_context(self, context):
        for page in FundraisingPage.objects.all():
            self.children.append(page)

class CRMStatsModule(modules.DashboardModule):
    def is_empty():
        return false
    #title = "Statistics"
    template = "progress_crm/stats_module.html"

    def init_with_context(self, context):
        context['total_people'] = Person.objects.count()
        context['total_events'] = Event.objects.count()
        context['total_donations'] = Donation.objects.count()
        context['total_donation_amount'] = Donation.objects.aggregate(Sum('amount'))['amount__sum']


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
    title = 'ProgressCRM'

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.Group(
                title="Control Panel",
                display="tabs",
                children=[
                    CRMStatsModule('Statistics'),
                    modules.ModelList('Database',self.models)
                ]
            ),
            CRMFundraisingModule('Fundraising Pages'),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]