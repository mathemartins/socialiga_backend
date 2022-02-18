import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

# from .forms import VideoForm
from django.views.generic import RedirectView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from analytics.models import EventViewEvent
from event.api.mixins import StaffMemberRequiredAPIMixin, AccountTypeCUSTOMERORVENDORAPIMixin

from event.api.serializers import EventCreateSerializer
from event.models import Event, MyEvents


class EventCreateAPIView(StaffMemberRequiredAPIMixin, AccountTypeCUSTOMERORVENDORAPIMixin, CreateAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    model = Event
    serializer_class = EventCreateSerializer

    def perform_create(self, serializer):
        serializer.partial = True
        serializer.save(user=self.request.user)


class EventDetailAPIView(RetrieveAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = EventCreateSerializer
    model = Event
    lookup_field = 'slug'

    # queryset = Course.objects.all()
    def get_object(self):
        slug = self.kwargs.get("slug")
        qs = Event.objects.filter(slug=slug).owned(self.request.user)
        if qs.exists():
            obj = qs.first()
            if self.request.user.is_authenticated:
                view_event, created = EventViewEvent.objects.get_or_create(user=self.request.user, event=obj)
                if view_event:
                    view_event.views += 1
                    view_event.save()
            return obj
        return Response({"message": "Does not exist!"}, status=404)

    def get(self, request, *args, **kwargs):
        print(args, kwargs, self.get_object())
        if not self.get_object().is_owner:
            return Response({"message": "You must purchase this event to attend"}, status=401)
        return self.retrieve(request, *args, **kwargs)


class EventPurchaseAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permanent = False

    def get(self, request, *args, **kwargs):
        qs = Event.objects.filter(slug=kwargs.get('slug')).owned(request.user)
        print(qs)
        if qs.exists():
            user = self.request.user
            if user.is_authenticated:
                my_events = user.myevents
                # run transaction
                # if transaction successful:
                my_events.events.add(qs.first())
                return Response(
                    {"message": "Congratulations! On purchasing this event",
                     "event_path": qs.first().get_absolute_url()},
                    status=200
                )
            # if user already owns course, take user to the course
            return Response(
                {"message": "You already own this event", "event_path": qs.first().get_absolute_url()},
                status=200
            )
        return Response({"message": "Redirect to payment processing gateway"}, status=200)


class EventListAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = EventCreateSerializer
    paginate_by = 12

    def get_serializer_context(self, *args, **kwargs):
        context = super(EventListAPIView, self).get_serializer_context(*args, **kwargs)
        print(dir(context.get('page_obj')), context)
        return {'request': self.request}

    def get_queryset(self):
        request = self.request
        qs = Event.objects.all()
        query = request.GET.get('q')
        user = self.request.user
        if query:
            qs = qs.filter(title__icontains=query)
        if user.is_authenticated:
            qs = qs.owned(user)
        return qs


class EventUpdateAPIView(StaffMemberRequiredAPIMixin, UpdateAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        obj = serializer.save(commit=False)
        if not self.request.user.is_staff:
            obj.user = self.request.user
        obj.save()

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = Event.objects.filter(slug=slug)
        if obj.exists():
            return obj.first()
        return Response({"message": "Does not exist"}, status=404)


class EventDeleteAPIView(StaffMemberRequiredAPIMixin, DestroyAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    queryset = Event.objects.all()
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = Event.objects.filter(slug=slug)
        if obj.exists():
            return obj.first()
        return Response({"message": "Does not exist"}, status=404)
