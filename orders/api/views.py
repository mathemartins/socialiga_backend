from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.views.generic import View, ListView, DetailView
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from billing.models import BillingProfile
from orders.api.serializers import OrderSerializer
from orders.models import Order, ProductPurchase


class OrderListAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_class = IsAuthenticated
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OrderDetailAPIView(RetrieveAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_class = IsAuthenticated
    serializer_class = OrderSerializer

    def get_object(self):
        qs = Order.objects.by_request(self.request).filter(
            order_id=self.kwargs.get('order_id')
        )
        if qs.count() == 1:
            return qs.first()
        return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class LibraryView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_class = IsAuthenticated
    serializer_class = OrderSerializer

    def get_queryset(self):
        return ProductPurchase.objects.products_by_request(self.request)  # .by_request(self.request).digital()


class VerifyOwnership(APIView):
    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.GET
        product_id = request.GET.get('product_id', None)
        if product_id is not None:
            product_id = int(product_id)
            ownership_ids = ProductPurchase.objects.products_by_id(request)
            if product_id in ownership_ids:
                return JsonResponse({'owner': True})
        return Response({'owner': False})
