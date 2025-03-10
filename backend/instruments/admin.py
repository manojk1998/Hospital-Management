from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import InstrumentCategory, Instrument, InstrumentMaintenance


class InstrumentMaintenanceInline(admin.TabularInline):
    model = InstrumentMaintenance
    extra = 0


@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


@admin.register(Instrument)
class InstrumentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'serial_number', 'category', 'status', 'purchase_date', 'purchase_price', 'rental_price_per_day', 'selling_price')
    list_filter = ('status', 'category', 'purchase_date')
    search_fields = ('name', 'serial_number', 'description')
    readonly_fields = ('qr_code',)
    inlines = [InstrumentMaintenanceInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'serial_number', 'category', 'description', 'status')
        }),
        ('Financial Information', {
            'fields': ('purchase_date', 'purchase_price', 'rental_price_per_day', 'selling_price')
        }),
        ('Additional Information', {
            'fields': ('manufacturer', 'warranty_expiry', 'notes', 'image', 'qr_code')
        }),
    )


@admin.register(InstrumentMaintenance)
class InstrumentMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('instrument', 'maintenance_date', 'performed_by', 'cost', 'next_maintenance_date')
    list_filter = ('maintenance_date', 'next_maintenance_date')
    search_fields = ('instrument__name', 'instrument__serial_number', 'description', 'performed_by')
