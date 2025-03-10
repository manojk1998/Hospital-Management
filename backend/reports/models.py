from django.db import models
from django.utils import timezone
from accounts.models import User


class Report(models.Model):
    """Model for reports."""
    
    REPORT_TYPES = (
        ('sales', 'Sales Report'),
        ('rentals', 'Rentals Report'),
        ('inventory', 'Inventory Report'),
        ('revenue', 'Revenue Report'),
        ('clients', 'Clients Report'),
        ('staff', 'Staff Report'),
        ('custom', 'Custom Report'),
    )
    
    FORMAT_CHOICES = (
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    )
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True, null=True)
    parameters = models.JSONField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    file = models.FileField(upload_to='reports/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"


class Dashboard(models.Model):
    """Model for dashboards."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_dashboards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', 'name']
    
    def __str__(self):
        return self.name


class Widget(models.Model):
    """Model for dashboard widgets."""
    
    WIDGET_TYPES = (
        ('chart', 'Chart'),
        ('table', 'Table'),
        ('metric', 'Metric'),
        ('list', 'List'),
    )
    
    CHART_TYPES = (
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('pie', 'Pie Chart'),
        ('doughnut', 'Doughnut Chart'),
        ('area', 'Area Chart'),
    )
    
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    title = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=10, choices=WIDGET_TYPES)
    chart_type = models.CharField(max_length=10, choices=CHART_TYPES, blank=True, null=True)
    data_source = models.CharField(max_length=100)
    query_parameters = models.JSONField(blank=True, null=True)
    position_x = models.PositiveSmallIntegerField(default=0)
    position_y = models.PositiveSmallIntegerField(default=0)
    width = models.PositiveSmallIntegerField(default=1)
    height = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['dashboard', 'position_y', 'position_x']
    
    def __str__(self):
        return f"{self.title} ({self.dashboard.name})"
