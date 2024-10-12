import django.db.models.deletion
from django.db import migrations, models
class Migration(migrations.Migration):

    dependencies = [
        ('insurance_app', '0003_add_policies_with_premium_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NEW', 'New'), ('QUOTED', 'Quoted'), ('LIVE', 'Live')], default='NEW', max_length=10)),
                ('premium', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cover', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_app.customer')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_app.policy')),
            ],
        ),
        migrations.CreateModel(
            name='PolicyHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_status', models.CharField(max_length=10)),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='insurance_app.quote')),
            ],
        ),
    ]
