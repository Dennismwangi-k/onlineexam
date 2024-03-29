from django.contrib import admin

from subscriptions.models import (MpesaCheckoutRequest, MpesaResponseData,
                                  MpesaTransaction, Subscription,
                                  SubscriptionPackage)


@admin.register(MpesaCheckoutRequest)
class MpesaCheckoutRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "PhoneNumber", "AmountExpected", "MerchantRequestID", "CheckoutRequestID", "ResponseCode", "ResponseDescription", "CustomerMessage"]

# Register your models here.
@admin.register(SubscriptionPackage)
class SubscriptionPackageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "package", "start_date", "end_date"]


@admin.register(MpesaResponseData)
class MpesaResponseDataAdmin(admin.ModelAdmin):
    list_display = ["id", "response_data", "response_description", "response_code"]


@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "MerchantRequestID", "MpesaUser", "CheckoutRequestID", "ResultCode", "ResultDesc", "Amount", "TransactionTimeStamp", "TransactionDate", "PhoneNumber", "MpesaReceiptNumber"]
