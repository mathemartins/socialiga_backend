from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from blog.api.serializers import BlogPostSerializer
from blog.models import BlogPost


class BlogPostListAPIView(generics.ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = BlogPost.objects.all().published()
    serializer_class = BlogPostSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class BlogPostRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "slug"
