from django.db import models
from django.utils import timezone
from accounts.models import User
from clients.models import Client
from instruments.models import Instrument


class Order(models.Model):
    """Model for orders."""
    
    ORDER_TYPES = (
        ('sale', 'Sale'),
        ('rental', 'Rental'),
        ('storage', 'Storage'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('refunded', 'Refunded'),
    )
    
    order_number = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order_date']
    
    def __str__(self):
        return f"{self.order_number} - {self.client.hospital_name}"
    
    def save(self, *args, **kwargs):
        # Generate order number if not provided
        if not self.order_number:
            prefix = 'S' if self.order_type == 'sale' else 'R' if self.order_type == 'rental' else 'ST'
            date_str = timezone.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__startswith=f"{prefix}{date_str}").order_by('-order_number').first()
            
            if last_order:
                last_number = int(last_order.order_number[9:])
                new_number = last_number + 1
            else:
                new_number = 1
                
            self.order_number = f"{prefix}{date_str}{new_number:04d}"
        
        # Calculate grand total
        self.grand_total = self.total_amount + self.tax_amount - self.discount_amount
        
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Model for order items."""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_start_date = models.DateField(blank=True, null=True)
    rental_end_date = models.DateField(blank=True, null=True)
    rental_duration_days = models.PositiveIntegerField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.instrument.name} - {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        # Calculate subtotal
        if self.order.order_type == 'rental' and self.rental_duration_days:
            self.subtotal = self.unit_price * self.quantity * self.rental_duration_days
        else:
            self.subtotal = self.unit_price * self.quantity
        
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Model for payments."""
    
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('cheque', 'Cheque'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_payments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment for {self.order.order_number} - {self.amount}"


class Invoice(models.Model):
    """Model for invoices."""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    billing_address = models.TextField()
    shipping_address = models.TextField(blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-invoice_date']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        # Generate invoice number if not provided
        if not self.invoice_number:
            date_str = timezone.now().strftime('%Y%m%d')
            last_invoice = Invoice.objects.filter(invoice_number__startswith=f"INV{date_str}").order_by('-invoice_number').first()
            
            if last_invoice:
                last_number = int(last_invoice.invoice_number[11:])
                new_number = last_number + 1
            else:
                new_number = 1
                
            self.invoice_number = f"INV{date_str}{new_number:04d}"
        
        super().save(*args, **kwargs)
