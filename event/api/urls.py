from django.conf.urls import url
from event.api.views import EventCreateAPIView, EventListAPIView, EventDetailAPIView, \
    EventUpdateAPIView, EventPurchaseAPIView, EventDeleteAPIView

urlpatterns = [
    url(r'^$', EventListAPIView.as_view(), name='list'),
    url(r'^create/(?P<slug>[\w-]+)/course/$', EventCreateAPIView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', EventDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/purchase/$', EventPurchaseAPIView.as_view(), name='purchase'),
    url(r'^(?P<slug>[\w-]+)/edit/$', EventUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', EventDeleteAPIView.as_view(), name='delete'),
]