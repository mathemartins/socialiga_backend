from django.contrib import admin

# Register your models here.
from event.models import Event, MyEvents

admin.site.register(MyEvents)


class EventAdmin(admin.ModelAdmin):
    list_filter = ['updated', 'timestamp']
    list_display = ['title', 'updated', 'timestamp', 'discounts']
    readonly_fields = ['updated', 'timestamp', 'short_title']
    search_fields = ['title', 'description']
    list_editable = ['discounts']
    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = Event

    def short_title(self, obj):
        return obj.title[:3]


admin.site.register(Event, EventAdmin)
