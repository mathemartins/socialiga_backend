from django.conf.urls import url

from .views import (
        ProductListAPIView,
        ProductDetailSlugAPIView,
        UserProductHistoryAPIView,
        ProductFeaturedRetrieveAPIView,
        ProductFeaturedListAPIView,
        ProductCreateAPIView

    )

urlpatterns = [
    url(r'^$', ProductListAPIView.as_view(), name='list'),
    url(r'^create/$', ProductCreateAPIView.as_view(), name='create'),
    url(r'^featured/$', ProductFeaturedListAPIView.as_view(), name='featured'),
    url(r'^featured/(?P<slug>[\w-]+)/$', ProductFeaturedRetrieveAPIView.as_view(), name='featured'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugAPIView.as_view(), name='detail'),
    url(r'^(?P<uslug>[\w-]+)/(?P<slug>[\w-]+)/$', UserProductHistoryAPIView.as_view(), name='user-slug'),
]