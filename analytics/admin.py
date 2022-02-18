from django.contrib import admin

# Register your models here.
from analytics.models import EventViewEvent

admin.site.register(EventViewEvent)