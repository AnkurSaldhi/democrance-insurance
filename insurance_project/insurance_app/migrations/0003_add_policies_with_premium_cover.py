# insurance_app/migrations/0003_add_policies_with_premium_cover.py
from django.db import migrations

def create_policies(apps, schema_editor):
    Policy = apps.get_model('insurance_app', 'Policy')

    # List of initial policy records with realistic premium and cover values
    insurance_types = [
        ("Personal Accident", "personal-accident", 120.00, 50000.00),
        ("Health Insurance", "health-insurance", 500.00, 100000.00),
        ("Life Insurance", "life-insurance", 1000.00, 250000.00),
        ("Home Insurance", "home-insurance", 300.00, 200000.00),
        ("Auto Insurance", "auto-insurance", 450.00, 150000.00),
    ]

    # Loop over the insurance types and create Policy records with premium and cover values
    for name, type_, premium, cover in insurance_types:
        Policy.objects.create(name=name, type=type_, premium=premium, cover=cover)

class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0002_policy')
    ]

    operations = [
        migrations.RunPython(create_policies, reverse_code=migrations.RunPython.noop),
    ]
