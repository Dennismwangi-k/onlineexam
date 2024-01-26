from django.urls import path

from subscriptions.apis.views import (LipaNaMpesaAPIView,
                                      LipaNaMpesaCallbackAPIView)

urlpatterns = [
    path("lipa-na-mpesa/", LipaNaMpesaAPIView.as_view(), name="lipa-na-mpesa"),
    path("lipa-na-mpesa-callback/", LipaNaMpesaCallbackAPIView.as_view(), name="lipa-na-mpesa-callback"),
]