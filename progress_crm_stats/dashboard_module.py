from django.db.models import Sum
from progress_crm.plugins import CRMDashboardModule
from progress_crm.models import Person, Event, Donation

class CRMStatsModule(CRMDashboardModule):
    title = 'Reporting'

    def is_empty():
        return false

    #title = "Statistics"
    template = "progress_crm/stats_module.html"

    def init_with_context(self, context):
        context['total_people'] = Person.objects.count()
        context['total_events'] = Event.objects.count()
        context['total_donations'] = Donation.objects.count()
        context['total_donation_amount'] = Donation.objects.aggregate(Sum('amount'))['amount__sum']