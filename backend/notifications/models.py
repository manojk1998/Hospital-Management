from django.db import models
from django.utils import timezone
from accounts.models import User


class Notification(models.Model):
    """Model for notifications."""
    
    TYPE_CHOICES = (
        ('payment_due', 'Payment Due'),
        ('payment_received', 'Payment Received'),
        ('order_status', 'Order Status Update'),
        ('rental_expiry', 'Rental Expiry'),
        ('maintenance_due', 'Maintenance Due'),
        ('stock_alert', 'Stock Alert'),
        ('system', 'System Notification'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    related_object_type = models.CharField(max_length=50, blank=True, null=True)
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
    
    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class EmailNotification(models.Model):
    """Model for email notifications."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )
    
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    html_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    related_object_type = models.CharField(max_length=50, blank=True, null=True)
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.recipient_email}"


class SMSNotification(models.Model):
    """Model for SMS notifications."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )
    
    recipient_number = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    related_object_type = models.CharField(max_length=50, blank=True, null=True)
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"SMS to {self.recipient_number}"
