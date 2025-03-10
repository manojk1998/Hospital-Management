from django.contrib import admin
from .models import Notification, EmailNotification, SMSNotification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'priority', 'is_read', 'created_at')
    list_filter = ('notification_type', 'priority', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__email')
    readonly_fields = ('created_at', 'read_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'message', 'notification_type', 'priority')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at')
        }),
        ('Related Object', {
            'fields': ('related_object_type', 'related_object_id')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'recipient_email', 'status', 'sent_at', 'created_at')
    list_filter = ('status', 'created_at', 'sent_at')
    search_fields = ('subject', 'message', 'recipient_email')
    readonly_fields = ('created_at', 'sent_at')
    fieldsets = (
        (None, {
            'fields': ('recipient_email', 'subject', 'message', 'html_message')
        }),
        ('Status', {
            'fields': ('status', 'sent_at', 'error_message')
        }),
        ('Related Object', {
            'fields': ('related_object_type', 'related_object_id')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(SMSNotification)
class SMSNotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient_number', 'message', 'status', 'sent_at', 'created_at')
    list_filter = ('status', 'created_at', 'sent_at')
    search_fields = ('recipient_number', 'message')
    readonly_fields = ('created_at', 'sent_at')
    fieldsets = (
        (None, {
            'fields': ('recipient_number', 'message')
        }),
        ('Status', {
            'fields': ('status', 'sent_at', 'error_message')
        }),
        ('Related Object', {
            'fields': ('related_object_type', 'related_object_id')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
