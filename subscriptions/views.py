from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from subscriptions.models import (MpesaResponseData, MpesaTransaction,
                                  Subscription)
from subscriptions.utils import MpesaGateWay
from subscriptions.validators import validate_possible_number


# Create your views here.
@login_required(login_url="/accounts/login/")
def pay_subscription(request):
    user = request.user
    if request.method == "POST":
        amount = request.POST.get("amount")
        phone_number = request.POST.get("phone_number")

        valid_phone_number = validate_possible_number(phone_number)

        mpesa = MpesaGateWay()
        mpesa.stk_push(
            phone_number=valid_phone_number,
            amount=int(amount),
            callback_url=f"{settings.BACKEND_URL}/subscriptions/lipa-na-mpesa-callback/",
            account_reference="Exam subscription payments!!",
            transaction_desc="This is a student exam subscription payment.",
            user_email=user.email
        )


        print(f"Phone: {phone_number}, Valid Phone: {valid_phone_number}, Amount: {amount}")

    return render(request, "subscriptions/pay_subscription.html")


def verify_mpesa_transaction(request):
    if request.method == "POST":
        checkout_id = request.POST.get("checkout_id")

        mpesa = MpesaGateWay()
        mpesa.verify_transaction(checkout_id=checkout_id)

    return render(request, "subscriptions/verify_transaction.html")