# Generated by Django 4.2.3 on 2024-10-16 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_customer_mobile_checkout"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkout",
            name="quotation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.quotationform",
            ),
        ),
    ]
