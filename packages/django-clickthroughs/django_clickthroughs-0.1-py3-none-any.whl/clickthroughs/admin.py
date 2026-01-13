from django.contrib import admin

from .models import *


## inlines --------------------------------------------------------------------


class CampaignHostnameInline(admin.TabularInline):
    model = CampaignHostname
    extra = 1


## admins ---------------------------------------------------------------------


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):

    list_display = ['name']


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'start_date', 'end_date']
    prepopulated_fields = {'slug': ['name']}
    inlines = [CampaignHostnameInline]


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):

    list_display = ['platform', 'key', 'value']
    list_filter = ['platform']


@admin.register(Clickthrough)
class ClickthroughAdmin(admin.ModelAdmin):

    list_display = ['clicked_at', 'hostname', 'url_to']
