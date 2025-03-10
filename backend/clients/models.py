from django.db import models
from accounts.models import User


class Client(models.Model):
    """Model for hospital clients."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    hospital_name = models.CharField(max_length=200)
    hospital_type = models.CharField(max_length=100, choices=[
        ('government', 'Government'),
        ('private', 'Private'),
        ('non_profit', 'Non-Profit'),
        ('research', 'Research'),
        ('teaching', 'Teaching'),
    ])
    registration_number = models.CharField(max_length=100, unique=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    bed_count = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['hospital_name']
    
    def __str__(self):
        return self.hospital_name


class ClientContact(models.Model):
    """Model for hospital client contacts."""
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.client.hospital_name})"


class ClientAddress(models.Model):
    """Model for hospital client addresses."""
    
    ADDRESS_TYPES = (
        ('billing', 'Billing Address'),
        ('shipping', 'Shipping Address'),
        ('both', 'Both Billing & Shipping'),
    )
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='both')
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    is_default = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default']
        verbose_name_plural = 'Client Addresses'
    
    def __str__(self):
        return f"{self.client.hospital_name} - {self.get_address_type_display()}"
