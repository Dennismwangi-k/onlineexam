import json
from datetime import datetime, timedelta

from exam.models import ExamUser
from subscriptions.models import (MpesaCheckoutRequest, Subscription,
                                  SubscriptionPackage)
from subscriptions.utils import MpesaGateWay
from subscriptions.validators import validate_possible_number

date_today = datetime.now().date()
next_date = date_today + timedelta(days=365)


class ProcessSubscriptionMixin(object):
    def __init__(self, email):
        self.email = email

    def run(self):
        self.__process_subscription()

    def __process_subscription(self):
        print("**********Transactions Are Being Checked on the background!!!")
        try:
            user = ExamUser.objects.get(email=self.email)

            checkout_requests = MpesaCheckoutRequest.objects.filter(
                ProcessingStatus="Processed Unsuccessfully", processed=False).filter(
                    UserEmail=self.email).order_by("-created")[:5]

            if checkout_requests.count() >= 1:

                for checkout_req in checkout_requests:
                    subscription = Subscription.objects.filter(user=user).first()

                    if not subscription:
                        subscription = Subscription.objects.create(
                            user=user,
                            start_date=date_today,
                            end_date=next_date,
                            status="Active"
                        )

                    package = SubscriptionPackage.objects.get(
                        name__in=["Pro Plan", "Pro"])

                    mpesa = MpesaGateWay()
                    res = mpesa.verify_transaction(
                        checkout_id=checkout_req.CheckoutRequestID)

                    res_data = json.loads(res.text)

                    if res_data["ResultCode"] in [200, 201]:
                        subscription.status = "Active"
                        subscription.package = package
                        subscription.save()

                        checkout_req.processed = True
                        checkout_req.ProcessingStatus="Processed Successfully"
                        checkout_req.save()

                        user.subscription_active = True
                        user.save()

                    else:
                        checkout_req.ProcessingStatus="Processed Successfully"
                        checkout_req.save()
        except Exception as e:
            raise e