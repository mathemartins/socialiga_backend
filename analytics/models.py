from django.conf import settings
from django.db import models


# Create your models here.
from event.models import Event


class EventViewEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.views)
