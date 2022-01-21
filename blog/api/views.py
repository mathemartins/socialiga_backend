from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from rest_framework import generics

from blog.api.serializers import BlogPostSerializer
from blog.models import BlogPost


class BlogPostListAPIView(generics.ListAPIView):
    queryset = BlogPost.objects.all().published()
    serializer_class = BlogPostSerializer

    def get_serializer_context(self):
        return {'request': self.request}


# @staff_member_required
# def blog_post_create_view(request):
#     # create objects
#     # ? use a form
#     # request.user -> return something
#     form = BlogPostModelForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = request.user
#         obj.save()
#         form = BlogPostModelForm()
#     template_name = 'form.html'
#     context = {'form': form}
#     return render(request, template_name, context)


# def blog_post_detail_view(request, slug):
#     # 1 object -> detail view
#     obj = get_object_or_404(BlogPost, slug=slug)
#     template_name = 'blog/detail.html'
#     context = {"object": obj}
#     return render(request, template_name, context)
#
#
# @staff_member_required
# def blog_post_update_view(request, slug):
#     obj = get_object_or_404(BlogPost, slug=slug)
#     form = BlogPostModelForm(request.POST or None, instance=obj)
#     if form.is_valid():
#         form.save()
#     template_name = 'form.html'
#     context = {"title": f"Update {obj.title}", "form": form}
#     return render(request, template_name, context)
#
#
# @staff_member_required
# def blog_post_delete_view(request, slug):
#     obj = get_object_or_404(BlogPost, slug=slug)
#     template_name = 'blog/delete.html'
#     if request.method == "POST":
#         obj.delete()
#         return redirect("/blog")
#     context = {"object": obj}
#     return render(request, template_name, context)
