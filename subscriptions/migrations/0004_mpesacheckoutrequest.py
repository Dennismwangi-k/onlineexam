# Generated by Django 5.0 on 2024-01-31 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0003_subscription_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="MpesaCheckoutRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("MerchantRequestID", models.CharField(max_length=255)),
                ("CheckoutRequestID", models.CharField(max_length=255)),
                ("ResultCode", models.IntegerField(default=0)),
                ("ResultDescription", models.CharField(max_length=1000)),
                ("CustomerMessage", models.CharField(max_length=100)),
            ],
        ),
    ]