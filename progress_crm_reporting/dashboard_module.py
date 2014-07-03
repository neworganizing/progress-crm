from django.db.models import Sum, Count
from progress_crm.plugins import CRMDashboardModule
#from progress_crm.models import Person, Event, Donation, List

class CRMReportingModule(CRMDashboardModule):
    title = 'Reporting'

    def is_empty():
        return False

    template = "progress_crm_reporting/reporting_module.html"

    def init_with_context(self, context):
        super(CRMReportingModule, self).init_with_context(context)