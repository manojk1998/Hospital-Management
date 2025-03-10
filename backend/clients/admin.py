from django.contrib import admin
from .models import Client, ClientContact, ClientAddress


class ClientContactInline(admin.TabularInline):
    model = ClientContact
    extra = 1


class ClientAddressInline(admin.TabularInline):
    model = ClientAddress
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('hospital_name', 'hospital_type', 'registration_number', 'is_active', 'created_at')
    list_filter = ('hospital_type', 'is_active', 'created_at')
    search_fields = ('hospital_name', 'registration_number', 'tax_id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ClientContactInline, ClientAddressInline]
    fieldsets = (
        (None, {
            'fields': ('user', 'hospital_name', 'hospital_type', 'registration_number')
        }),
        ('Additional Information', {
            'fields': ('tax_id', 'website', 'established_date', 'bed_count', 'is_active', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ClientContact)
class ClientContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'position', 'email', 'phone', 'is_primary')
    list_filter = ('is_primary', 'client')
    search_fields = ('name', 'email', 'phone', 'client__hospital_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ClientAddress)
class ClientAddressAdmin(admin.ModelAdmin):
    list_display = ('client', 'address_type', 'city', 'state', 'country', 'is_default')
    list_filter = ('address_type', 'is_default', 'country', 'state')
    search_fields = ('client__hospital_name', 'street_address', 'city', 'state', 'postal_code')
    readonly_fields = ('created_at', 'updated_at')
