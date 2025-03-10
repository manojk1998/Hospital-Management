from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, EmailNotificationViewSet, SMSNotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'emails', EmailNotificationViewSet, basename='email-notification')
router.register(r'sms', SMSNotificationViewSet, basename='sms-notification')

urlpatterns = [
    path('', include(router.urls)),
] 