# Generated by Django 5.0.1 on 2024-01-18 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bucketapp', '0003_remove_onetimepayment_budgeted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
