from django.contrib import admin
from .models import Order, OrderItem, Payment, Invoice


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('subtotal', 'created_at', 'updated_at')


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'client', 'order_type', 'status', 'payment_status', 'order_date', 'grand_total')
    list_filter = ('order_type', 'status', 'payment_status', 'order_date')
    search_fields = ('order_number', 'client__hospital_name', 'notes')
    readonly_fields = ('order_number', 'grand_total', 'created_at', 'updated_at')
    inlines = [OrderItemInline, PaymentInline]
    fieldsets = (
        (None, {
            'fields': ('order_number', 'client', 'order_type', 'status', 'payment_status')
        }),
        ('Dates', {
            'fields': ('order_date', 'delivery_date')
        }),
        ('Financial Details', {
            'fields': ('total_amount', 'tax_amount', 'discount_amount', 'grand_total')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'instrument', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('order__order_type', 'order__status')
    search_fields = ('order__order_number', 'instrument__name', 'instrument__serial_number')
    readonly_fields = ('subtotal', 'created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'status', 'payment_date')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ('order__order_number', 'transaction_id', 'notes')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'order', 'status', 'invoice_date', 'due_date')
    list_filter = ('status', 'invoice_date', 'due_date')
    search_fields = ('invoice_number', 'order__order_number', 'notes')
    readonly_fields = ('invoice_number', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('invoice_number', 'order', 'status')
        }),
        ('Dates', {
            'fields': ('invoice_date', 'due_date')
        }),
        ('Addresses', {
            'fields': ('billing_address', 'shipping_address')
        }),
        ('Additional Information', {
            'fields': ('terms_and_conditions', 'notes', 'pdf_file')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
