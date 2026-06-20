from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Member)

admin.site.register(Products)

class IncidentProgressInline(admin.TabularInline):
    model = IncidentProgress
    extra = 1
    fields = (
        'status',
        'note',
        'created_by',
        'created_at'
    )
    readonly_fields = ('created_at',)


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'title',
        'category',
        'priority',
        'status',
        'reporter_name',
        'created_at',
    )

    list_filter = (
        'status',
        'category',
        'priority',
        'created_at',
    )

    search_fields = (
        'code',
        'title',
        'location',
        'reporter_name',
        'reporter_phone',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    inlines = [IncidentProgressInline]


@admin.register(IncidentProgress)
class IncidentProgressAdmin(admin.ModelAdmin):

    list_display = (
        'incident',
        'status',
        'created_by',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'incident__code',
        'note',
    )



