from django.contrib import admin

# Register your models here.
from analytics.models import EventViewEvent, ObjectViewed, UserSession

admin.site.register(EventViewEvent)
admin.site.register(ObjectViewed)
admin.site.register(UserSession)