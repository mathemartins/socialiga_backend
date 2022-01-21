from django.contrib.auth import get_user_model
from django.utils.text import Truncator
from rest_framework import serializers
from blog.models import BlogPost

User = get_user_model()


class BlogPostSerializer(serializers.ModelSerializer):
    image_uri = serializers.SerializerMethodField(read_only=True)
    content = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'user',
            'image',
            'image_uri',
            'title',
            'slug',
            'content',
            'publish_date',
            'timestamp',
            'updated',
        ]

    def get_image_uri(self, obj: BlogPost):
        instance = BlogPost.objects.get(slug=obj.slug)
        if instance.image:
            return instance.image.url
        return None

    def get_content(self, obj: BlogPost):
        instance = BlogPost.objects.get(slug=obj.slug)
        return Truncator(instance.content).words(12)