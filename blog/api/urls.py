from django.urls import path
from blog.api.views import (
    BlogPostListAPIView
)

urlpatterns = [
    path('', BlogPostListAPIView.as_view(), name='blog-post-list'),
    # path('<str:slug>/', blog_post_detail_view),
    # path('<str:slug>/edit/', blog_post_update_view),
    # path('<str:slug>/delete/', blog_post_delete_view),
]