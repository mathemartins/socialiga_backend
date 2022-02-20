from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from billing.models import BillingProfile, Card
from billing.utils import PaystackAPI, SECRET_KEY

ps_instance = PaystackAPI(secret_key=SECRET_KEY)


class PaymentMethodAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return Response({"message": "No active or registered billing profile for user"}, status=403)
        billing_profile_qs = BillingProfile.objects.filter(user=request.user).values()
        card_qs = Card.objects.filter(billing_profile=billing_profile).values()
        message = {
            "billing": billing_profile_qs,
            "card": card_qs
        }
        return Response(message, status=200)


class PaymentMethodCreateAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return Response({"message": "Cannot find this user"}, status=401)
        card_data = request.data.get("card_data")
        if card_data is not None:
            new_card_obj = Card.objects.add_new(billing_profile, card_data)
        return Response({"message": "Success! Your card was added."}, status=200)

