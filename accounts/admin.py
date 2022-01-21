from django.contrib import admin

# Register your models here.
from accounts.models import EmailActivation, Profile, Address


class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = EmailActivation


admin.site.register(EmailActivation, EmailActivationAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'uuid', 'account_type', 'gender', 'phone', 'date_of_birth', 'slug', 'timestamp', 'updated')
    list_display_links = ('user',)
    list_filter = ('user',)
    search_fields = ('user', 'uuid')
    readonly_fields = ('image_tag',)
    prepopulated_fields = {'slug': ('user', 'uuid', 'phone',)}

    ordering = ('-timestamp',)
    fieldsets = (
        ('Basic Information', {'description': "User Profile Information",
                               'fields': (('user',), 'uuid', 'phone', 'image_tag', 'account_type')}),
        ('Complete Full Information',
         {'classes': ('collapse',), 'fields': ('slug', 'gender', 'date_of_birth')}),)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'street', 'locale', 'zip_code', 'state', 'country')
    list_display_links = ('user', 'street')
    list_editable = ('state', 'country')
    list_filter = ('state', 'country', 'zip_code')