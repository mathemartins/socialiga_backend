from django.urls import path
from blog.api.views import (
    BlogPostListAPIView, BlogPostRUDAPIView
)

urlpatterns = [
    path('', BlogPostListAPIView.as_view(), name='blog-post-list'),
    path('<str:slug>/', BlogPostRUDAPIView.as_view(), name='blog-post-retrieve-update-delete'),
]