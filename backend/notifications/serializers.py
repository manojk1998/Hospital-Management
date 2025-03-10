from rest_framework import serializers
from .models import Notification, EmailNotification, SMSNotification
from accounts.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at', 'read_at')


class EmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotification
        fields = '__all__'
        read_only_fields = ('created_at', 'sent_at')


class SMSNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSNotification
        fields = '__all__'
        read_only_fields = ('created_at', 'sent_at')


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at', 'read_at', 'is_read')


class EmailNotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotification
        fields = '__all__'
        read_only_fields = ('created_at', 'sent_at', 'status', 'error_message')


class SMSNotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSNotification
        fields = '__all__'
        read_only_fields = ('created_at', 'sent_at', 'status', 'error_message') 