from django.shortcuts import render

from subscriptions.models import (MpesaResponseData, MpesaTransaction,
                                  Subscription)
from subscriptions.validators import validate_possible_number


# Create your views here.
def pay_subscription(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        phone_number = request.POST.get("phone_number")

        valid_phone_number = validate_possible_number(phone_number)

        print(f"Phone: {phone_number}, Valid Phone: {valid_phone_number}, Amount: {amount}")

    return render(request, "subscriptions/pay_subscription.html")
