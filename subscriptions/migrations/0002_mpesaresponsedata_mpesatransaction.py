# Generated by Django 5.0 on 2024-01-26 07:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MpesaResponseData",
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
                ("response_data", models.JSONField(default=dict)),
                ("response_description", models.CharField(max_length=1000)),
                ("response_code", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="MpesaTransaction",
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
                ("MerchantRequestID", models.CharField(max_length=255)),
                ("CheckoutRequestID", models.CharField(max_length=255)),
                ("ResultCode", models.IntegerField(default=0)),
                ("ResultDesc", models.CharField(max_length=1000)),
                ("Amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("TransactionTimeStamp", models.CharField(max_length=255, null=True)),
                ("TransactionDate", models.DateTimeField()),
                ("PhoneNumber", models.CharField(max_length=255)),
                ("MpesaReceiptNumber", models.CharField(max_length=255)),
            ],
        ),
    ]