import json
import six
from rest_framework import serializers

from event.models import Event


class EventCreateSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'title',
            'slug',
            'image',
            'image_height',
            'image_width',
            'description',
            'price',
            'discounts',
            'active',
            'updated',
            'timestamp',
        ]
