from django.urls import re_path, path

from .views import UserDetailAPIView, UserAddressAPIView

urlpatterns = [
    path('address/', UserAddressAPIView.as_view(), name='address'),
    re_path(r'^(?P<username>\w+)/$', UserDetailAPIView.as_view(), name='detail'),
]