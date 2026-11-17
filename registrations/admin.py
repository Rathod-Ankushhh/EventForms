
import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Event, Registration, OrganizerProfile


# CSV Export Function
def export_registrations_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment; filename="registrations.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone', 'College', 'Event'])

    for registration in queryset:
        writer.writerow([
            registration.name,
            registration.email,
            registration.phone,
            registration.college,
            registration.event.name
        ])

    return response


# Event Approval Actions
@admin.action(description='Approve selected events')
def approve_events(modeladmin, request, queryset):
    queryset.update(status='approved')


@admin.action(description='Reject selected events')
def reject_events(modeladmin, request, queryset):
    queryset.update(status='rejected')


# Event Admin
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date',
        'venue',
        'available_seats',
        'organizer',
        'status'
    )
    list_filter = ('date', 'status')
    search_fields = ('name', 'venue')
    actions = [approve_events, reject_events]


# Registration Admin
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'college', 'event')
    list_filter = ('event',)
    search_fields = ('name', 'email', 'phone', 'college')
    actions = [export_registrations_csv]


# Organizer Profile Admin
@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_trusted')
    list_filter = ('is_trusted',)
    search_fields = ('user__username', 'user__email')
