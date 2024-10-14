from django.db import models
from .constants import POLICY_STATUS_CHOICES, INSURANCE_TYPES
# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Policy(models.Model):
    #Policy Name
    name = models.CharField(max_length=255)

    # Type of Policy
    type = models.CharField(max_length=50, choices=INSURANCE_TYPES, unique=True)

    # Default Premium for the policy, modified by age later when "Create Quote" gets called
    premium = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Default Cover for the policy, modified by age later when "Create Quote" gets called
    cover = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PolicyHistory(models.Model):
    """
    Row for this model gets created for every new row insert in Quote model or at every status change in Quote model
    """
    quote = models.ForeignKey('Quote', on_delete=models.CASCADE, related_name='history')  # Allow multiple history records for each quote
    last_status = models.CharField(max_length=10)  # Store the status of the quote
    changed_at = models.DateTimeField(auto_now_add=True)  # Capture when the status was changed

    def __str__(self):
        return f"History for Quote ID {self.quote.id}: {self.last_status} at {self.changed_at}"

class Quote(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    policy = models.ForeignKey('Policy', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=POLICY_STATUS_CHOICES, default='NEW')
    premium = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cover = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    buy_date = models.DateTimeField(null=True, blank=True)  # Date when the policy is bought i.e. status=LIVE
    expiry = models.DateTimeField(null=True, blank=True)  # Expiry date of the policy, set when policy goes LIVE
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Policy for {self.customer.first_name}(customer_id:{self.customer.id}) - {self.policy.name} (Status: {self.status})"

    def save(self, *args, **kwargs):
        is_new_quote = self.pk is None  # Check if this is a new quote

        if not is_new_quote:
            original = Quote.objects.get(pk=self.pk)  # Get the original quote before saving
            original_status = original.status  # Store the original status

        # Save the quote first to get the pk
        super().save(*args, **kwargs)

        # If this is a new quote, create the initial PolicyHistory record
        if is_new_quote:
            PolicyHistory.objects.create(
                quote=self,
                last_status=self.status  # Record the initial status
            )
        else:
            # If this is an update, check if the status has changed
            if original_status != self.status:
                # Create a new history record for the status change
                PolicyHistory.objects.create(
                    quote=self,
                    last_status=self.status  # Record the latest status
                )
