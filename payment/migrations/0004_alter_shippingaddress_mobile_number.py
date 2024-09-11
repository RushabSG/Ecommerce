# Generated by Django 5.0.6 on 2024-08-21 04:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0003_alter_shippingaddress_mobile_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shippingaddress",
            name="mobile_number",
            field=models.CharField(
                error_messages="Enter the valid Mobile Number",
                max_length=20,
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^(\\+?\\d{1,3})?[-.\\s]?\\(?\\d{3}\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{4}$"
                    )
                ],
            ),
        ),
    ]
