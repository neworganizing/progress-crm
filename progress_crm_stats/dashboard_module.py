from django.db.models import Sum, Count
from progress_crm.plugins import CRMDashboardModule
from progress_crm.models import Person, Event, Donation, List

class CRMStatsModule(CRMDashboardModule):
    title = 'Statistics'

    def is_empty():
        return false

    #title = "Statistics"
    template = "progress_crm_stats/stats_module.html"

    def init_with_context(self, context):
        context['lists'] = List.objects.all()
        context['total_people'] = Person.objects.count()
        context['total_events'] = Event.objects.count()
        context['total_donations'] = Donation.objects.count()

        total_donation_amount = Donation.objects.aggregate(Sum('amount'))['amount__sum']
        if not total_donation_amount:
            total_donation_amount = 0.0

        context['total_donation_amount'] = total_donation_amount
        context['state_counts'] = Person.objects.filter(
            personpostaladdress__primary=True,
            postal_addresses__region__regex=r'^[A-Za-z]{2}$'
        ).values(
            'postal_addresses__region'
        ).annotate(
            count=Count('postal_addresses__region')
        ).order_by('postal_addresses__region')