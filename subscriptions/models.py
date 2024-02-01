from django.db import models

from subscriptions.shared_methods import convert_timestamp_to_datetime

# Create your models here.
SUBSCRIPTION_STATUS_CHOICES = (
    ("Active", "Active"),
    ("Deactivated", "Deactivated"),
)

TRANSACTION_PROCESSING_STATUSES = (
    ("Processed Successfully", "Processed Successfully"),
    ("Processed Unsuccessfully", "Processed Unsuccessfully"),
)

class SubscriptionPackage(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.OneToOneField("exam.ExamUser", on_delete=models.CASCADE)
    package = models.ForeignKey(SubscriptionPackage, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=255, choices=SUBSCRIPTION_STATUS_CHOICES, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class MpesaResponseData(models.Model):
    response_data = models.JSONField(default=dict)
    response_description = models.CharField(max_length=1000)
    response_code = models.CharField(max_length=255)

    def __str__(self):
        return self.response_code


class MpesaTransaction(models.Model):
    MerchantRequestID = models.CharField(max_length=255)
    CheckoutRequestID = models.CharField(max_length=255)
    ResultCode = models.IntegerField(default=0)
    ResultDesc = models.CharField(max_length=1000)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    TransactionTimeStamp = models.CharField(max_length=255, null=True)
    TransactionDate = models.DateTimeField()
    PhoneNumber = models.CharField(max_length=255)
    MpesaReceiptNumber = models.CharField(max_length=255)
    MpesaUser = models.ForeignKey("exam.ExamUser", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.MpesaReceiptNumber

    
    def save(self, *args, **kwargs) -> None:
        self.TransactionDate = convert_timestamp_to_datetime(self.TransactionTimeStamp)
        return super().save(*args, **kwargs)


class MpesaCheckoutRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    MerchantRequestID = models.CharField(max_length=255)
    CheckoutRequestID = models.CharField(max_length=255)
    ResponseCode = models.IntegerField(default=0)
    ResponseDescription = models.CharField(max_length=1000)
    CustomerMessage = models.CharField(max_length=100)
    AmountExpected = models.IntegerField(default=0)
    PhoneNumber = models.CharField(max_length=255, null=True)
    ProcessingStatus = models.CharField(max_length=255, choices=TRANSACTION_PROCESSING_STATUSES, null=True)
    processed = models.BooleanField(default=False)
    UserEmail = models.EmailField(null=True)

    def __str__(self):
        return self.CheckoutRequestID
