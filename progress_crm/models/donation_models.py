from django.db import models
from django.core.exceptions import ValidationError
from jsonfield import JSONField

class Recipient(models.Model):
    '''
    Recipient
    ---------
    This model represents the recipient of a donation.  Mutliple recipients could be part of the
    same donation action, i.e. when doing "bundling"

    Fields
    ------
    display_name - The name to be displayed when viewing donation information
    legal_name - Name registered with the FEC, etc.
    amount - Amount of donation to this recipient
    '''
    display_name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=11)
    donation = models.ForeignKey('Donation', related_name='recipients')

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'progress_crm'

    def __unicode__(self):
        return self.display_name

PAYMENT_METHOD_CHOICES = (
    ("credit_card", "Credit Card"),
    ("check", "Check"),
    ("cash", "Cash"),
    ("electronic_funds_transfer", "Electronic Funds Transfer")
)

class FundraisingPage(models.Model):
    '''
    FundraisingPage
    ---------------
    Represents a page or action collecting one or more donations

    Fields
    ------
    identifiers - The OSDI identifiers of this page
    originating_system - Human readable text identifying where this page originated
    created_at - Date and Time of creation
    modified_at - Date and Time of last modification
    name - The name of the page
    title - The title of the page
    summary - The summary of the page
    description - The description of the page
    url - The URL of the fundraising page
    total_donations - Computed value of total donations made to the page
    total_revenue - Computed value of total donation revenue made to this page
    currency - ISO 4217 designation of currency. Example: USD, JPY
    creator - The person representing the creator of the fundraising page
    donations - Collection of donations made from this page
    '''
    identifiers = models.TextField()
    originating_system = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=1023)
    description = models.TextField(blank=True)
    url = models.URLField()
    currency = models.CharField(max_length=255)
    creator = models.ForeignKey('Person')
    #donations = reverse relationship

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    @property
    def total_donations(self):
        pass

    @property
    def total_revenue(self):
        pass

    class Meta:
        app_label='progress_crm'

    def __unicode__(self):
        return self.name

class Donation(models.Model):
    '''
    Donation
    --------
    This class represents a recorded donation.

    Fields
    ------
    identifiers - The OSDI identifiers of this donation
    created_at  - Date and Time of creation
    modified_at - Date and Time of last modification
    originating_system - The original donation system. Example: ActBlue
    donor - Donor data collected at the time of donation
    donated_at - Date of the donation
    amount - Amount of total donation (after any credits) in specified currency
    credited_amount - Amount credited back to donor in specified currency
    credited_at - Date of the credit
    currency - ISO 4217 designation of currency. Example: USD, JPY
    recipients - Array of recipients associated with the donation
    payment - A hash of payment details
    payment.method - A flexible enumeration of "Credit Card", "Check", "Cash", "Electronic Funds Transfer"
    payment.reference_number - A check number, transaction ID, or some other information referencing the payment
    payment.authorization_stored - Indicates if payment information has been stored for future automatic payments
    subscription_instance - A sequence number or some other value unique to this instance of the donation in the context of a subscription. Examples: 5, JAN-2014
    voided - Indicates if the donation has been voided
    voided_at - Date of the void
    url - URL at which the donation was taken
    sources - Array of sources associated with the donation
    attributions - Array of attributions associated with the donation
    fundraising_page - The related fundraising page the donation was taken on
    '''
    identifiers = models.TextField()
    originating_system = models.CharField(max_length=255)
    donor = models.ForeignKey('Person')
    donated_at = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=11)
    credited_amount = models.DecimalField(decimal_places=2, max_digits=11, null=True, blank=True)
    credited_at = models.DateTimeField(null=True, blank=True)
    currency = models.CharField(max_length = 255)
    # recipients - Reverse relationship
    payment = JSONField()
    ## Fields within payment hash
    #payment.method
    #payment.reference_number
    #payment.authorization_stored
    subscription_instance = models.CharField(max_length=255, blank=True, null=True)
    voided = models.BooleanField(default=False)
    voided_at = models.DateField(null=True, blank=True)
    url = models.URLField()
    sources = models.TextField(null=True, blank=True)
    attributions = models.TextField(null=True, blank=True)
    fundraising_page = models.ForeignKey('FundraisingPage', null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        app_label = 'progress_crm'

    def __unicode__(self):
        return "Donation by {0} of {1} on {2}".format(self.donor, self.amount, self.donated_at)