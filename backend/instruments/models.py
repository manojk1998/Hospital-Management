from django.db import models
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image


class InstrumentCategory(models.Model):
    """Model for instrument categories."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Instrument Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Instrument(models.Model):
    """Model for hospital instruments."""
    
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('sold', 'Sold'),
        ('stored', 'In Storage'),
        ('maintenance', 'Under Maintenance'),
    )
    
    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(InstrumentCategory, on_delete=models.CASCADE, related_name='instruments')
    description = models.TextField(blank=True, null=True)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='instruments/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    warranty_expiry = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.serial_number})"
    
    def save(self, *args, **kwargs):
        # Generate QR code if it doesn't exist
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"Instrument: {self.name}\nSerial: {self.serial_number}")
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            self.qr_code.save(f"qr_{self.serial_number}.png", File(buffer), save=False)
        
        super().save(*args, **kwargs)


class InstrumentMaintenance(models.Model):
    """Model for tracking instrument maintenance."""
    
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    performed_by = models.CharField(max_length=100)
    next_maintenance_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-maintenance_date']
    
    def __str__(self):
        return f"Maintenance for {self.instrument.name} on {self.maintenance_date}"
