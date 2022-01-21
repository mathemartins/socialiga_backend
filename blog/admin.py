from django.contrib import admin

# Register your models here.
from blog.models import BlogPost


@admin.register(BlogPost)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'slug', 'publish_date', 'updated')
    list_display_links = ('user', 'title')
    list_filter = ('timestamp', 'publish_date')
    search_fields = ('user', 'title', 'content')
    prepopulated_fields = {'slug': ('user', 'title')}

    ordering = ('-timestamp',)
