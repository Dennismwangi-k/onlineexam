from django.urls import path

from subscriptions.apis.views import (LipaNaMpesaAPIView,
                                      LipaNaMpesaCallbackAPIView)
from subscriptions.views import pay_subscription, verify_mpesa_transaction

urlpatterns = [
    path("pay-subscription/", pay_subscription, name="pay-subscription"),
    path("verify-transaction/", verify_mpesa_transaction, name="verify-transaction"),

    path("lipa-na-mpesa/", LipaNaMpesaAPIView.as_view(), name="lipa-na-mpesa"),
    path("lipa-na-mpesa-callback/", LipaNaMpesaCallbackAPIView.as_view(), name="lipa-na-mpesa-callback"),
]