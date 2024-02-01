from subscriptions.models import MpesaTransaction, Subscription, SubscriptionPackage
from exam.models import ExamUser
from datetime import datetime, timedelta

date_today = datetime.now().date()
next_date = date_today + timedelta(days=365)

class MpesaCallbackProcessMixin(object):
    def __init__(self, user_id, transaction_id):
        self.user_id = user_id
        self.transaction_id = transaction_id

    def run(self):
        self.__process_mpesa_callback()


    def __process_mpesa_callback(self):
        user = ExamUser.objects.get(id=self.user_id)
        transaction = MpesaTransaction.objects.get(id=self.transaction_id, MpesaUser=user)


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


        if transaction.ResultCode in ["0", 0]:
            subscription.status = "Active"
            subscription.package = package
            subscription.save()

            user.subscription_active = True
            user.save()
