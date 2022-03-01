from django.urls import re_path, path

from billing.api.views import PaymentMethodAPIView, PaymentMethodCreateAPIView

urlpatterns = [
    path('select-billing-profile/', PaymentMethodAPIView.as_view(), name='select-billing-profile'),
    path('add-card-profile/', PaymentMethodCreateAPIView.as_view(), name='create-billing-profile'),
]