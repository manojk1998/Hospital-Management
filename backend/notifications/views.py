from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Notification, EmailNotification, SMSNotification
from .serializers import (
    NotificationSerializer, NotificationCreateSerializer,
    EmailNotificationSerializer, EmailNotificationCreateSerializer,
    SMSNotificationSerializer, SMSNotificationCreateSerializer
)
from accounts.permissions import IsAdminUser, IsStaffUser, IsClientUser


class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing notifications.
    """
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'notification_type', 'priority', 'is_read']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Notification.objects.all()
        return Notification.objects.filter(user=self.request.user)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Mark a notification as read.
        """
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Mark all notifications as read for the current user.
        """
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        now = timezone.now()
        
        for notification in notifications:
            notification.is_read = True
            notification.read_at = now
            notification.save()
        
        return Response({"detail": f"Marked {notifications.count()} notifications as read."})


class EmailNotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing email notifications.
    """
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'recipient_email']
    search_fields = ['subject', 'message', 'recipient_email']
    ordering_fields = ['created_at', 'sent_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmailNotificationCreateSerializer
        return EmailNotificationSerializer
    
    def get_queryset(self):
        return EmailNotification.objects.all()
    
    def get_permissions(self):
        permission_classes = [IsAdminUser | IsStaffUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """
        Send an email notification.
        """
        email_notification = self.get_object()
        
        if email_notification.status == 'sent':
            return Response(
                {"detail": "This email has already been sent."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from django.core.mail import send_mail
            
            send_mail(
                subject=email_notification.subject,
                message=email_notification.message,
                from_email=None,  # Use DEFAULT_FROM_EMAIL from settings
                recipient_list=[email_notification.recipient_email],
                html_message=email_notification.html_message
            )
            
            email_notification.status = 'sent'
            email_notification.sent_at = timezone.now()
            email_notification.save()
            
            serializer = self.get_serializer(email_notification)
            return Response(serializer.data)
        
        except Exception as e:
            email_notification.status = 'failed'
            email_notification.error_message = str(e)
            email_notification.save()
            
            return Response(
                {"detail": f"Failed to send email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SMSNotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing SMS notifications.
    """
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'recipient_number']
    search_fields = ['message', 'recipient_number']
    ordering_fields = ['created_at', 'sent_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SMSNotificationCreateSerializer
        return SMSNotificationSerializer
    
    def get_queryset(self):
        return SMSNotification.objects.all()
    
    def get_permissions(self):
        permission_classes = [IsAdminUser | IsStaffUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """
        Send an SMS notification.
        
        Note: This is a placeholder implementation. In a real-world scenario,
        you would integrate with an SMS service provider like Twilio, AWS SNS, etc.
        """
        sms_notification = self.get_object()
        
        if sms_notification.status == 'sent':
            return Response(
                {"detail": "This SMS has already been sent."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Placeholder for SMS sending logic
            # In a real implementation, you would use an SMS service provider's API
            
            # For now, we'll just mark it as sent
            sms_notification.status = 'sent'
            sms_notification.sent_at = timezone.now()
            sms_notification.save()
            
            serializer = self.get_serializer(sms_notification)
            return Response(serializer.data)
        
        except Exception as e:
            sms_notification.status = 'failed'
            sms_notification.error_message = str(e)
            sms_notification.save()
            
            return Response(
                {"detail": f"Failed to send SMS: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
