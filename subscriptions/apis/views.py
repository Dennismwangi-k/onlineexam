
from django.conf import settings
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from subscriptions.apis.serializers import (LipaNaMpesaCallbackSerializer,
                                            LipaNaMpesaSerializer)
from subscriptions.models import MpesaResponseData, MpesaTransaction
from subscriptions.mpesa_callback_data import mpesa_callback_data_distructure
from subscriptions.utils import MpesaGateWay
from exam.models import ExamUser
from subscriptions.process_mpesa_callback import MpesaCallbackProcessMixin

BASE_BACKEND_URL = ""

class LipaNaMpesaCallbackAPIView(generics.CreateAPIView):
    serializer_class = LipaNaMpesaCallbackSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        user_id = request.query_params.get("user_id")

        print(f"User ID: {user_id}")

        print(f"Mpesa Data: {data}")
        

        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid(raise_exception=True):


            callback_data = mpesa_callback_data_distructure(data)
            mpesa_transaction = MpesaTransaction.objects.create(**callback_data)
            mpesa_transaction.save()

            user = ExamUser.objects.get(id=user_id)
            mpesa_transaction.MpesaUser = user
            mpesa_transaction.save()

            
            try:    
                mixin = MpesaCallbackProcessMixin(user_id=user_id, transaction_id=mpesa_transaction.id)
                mixin.run()
            except Exception as e:
                raise e
            

            print(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LipaNaMpesaAPIView(generics.CreateAPIView):
    serializer_class = LipaNaMpesaSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):  
            
            mpesa = MpesaGateWay()
            mpesa.stk_push(
                phone_number=data.get('phone_number'),
                amount=int(data.get("amount")),
                callback_url=f"{settings.BACKEND_URL}/payments/lipa-na-mpesa-callback/",
                account_reference="Online Exam Payments",
                transaction_desc="This is a subscription payment",
                user_email="admin@exams.com"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  