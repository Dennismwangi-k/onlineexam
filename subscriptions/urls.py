from django.urls import path

from subscriptions.apis.views import (LipaNaMpesaAPIView,
                                      LipaNaMpesaCallbackAPIView)
from subscriptions.views import pay_subscription

urlpatterns = [
    path("pay-subscription/", pay_subscription, name="pay-subscription"),
    path("lipa-na-mpesa/", LipaNaMpesaAPIView.as_view(), name="lipa-na-mpesa"),
    path("lipa-na-mpesa-callback/", LipaNaMpesaCallbackAPIView.as_view(), name="lipa-na-mpesa-callback"),
]