from django.conf.urls import url

from orders.api.views import (
        OrderListAPIView,
        OrderDetailAPIView,
        VerifyOwnership
        )

urlpatterns = [
    url(r'^$', OrderListAPIView.as_view(), name='list'),
    url(r'^endpoint/verify/ownership/$', VerifyOwnership.as_view(), name='verify-ownership'),
    url(r'^(?P<order_id>[0-9A-Za-z]+)/$', OrderDetailAPIView.as_view(), name='detail'),
]