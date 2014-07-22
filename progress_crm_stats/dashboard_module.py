from django.db.models import Sum, Count
from progress_crm.plugins import CRMDashboardModule
from progress_crm.models import Person, Event, Donation, List, ListItem

class CRMStatsModule(CRMDashboardModule):
    title = 'Statistics'

    def is_empty():
        return False

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

        list_growth_data = ListItem.objects.extra(
            select={'month': "strftime('%%m', datetime(created_at))"}
        ).filter(
            list_id=1, created_at__gte='2014-01-01'
        ).values('month'
        ).order_by('month'
        ).annotate(Count('id'))

        context['list_growth_data'] = [int(x['id__count']) for x in list_growth_data]