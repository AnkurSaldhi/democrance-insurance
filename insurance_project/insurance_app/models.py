from django.db import models

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
    INSURANCE_TYPES = [
        ('personal-accident', 'Personal Accident'),
        ('health-insurance', 'Health Insurance'),
        ('life-insurance', 'Life Insurance'),
        ('home-insurance', 'Home Insurance'),
        ('auto-insurance', 'Auto Insurance'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=INSURANCE_TYPES, unique=True)
    premium = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Premium for the policy
    cover = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)    # Coverage amount
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


