from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.utils import timezone
from .models import Order, OrderItem, Payment, Invoice
from .serializers import (
    OrderSerializer, OrderDetailSerializer, OrderCreateSerializer,
    OrderItemSerializer, PaymentSerializer, PaymentCreateSerializer,
    InvoiceSerializer, InvoiceCreateSerializer
)
from accounts.permissions import IsAdminUser, IsStaffUser, IsClientUser
from instruments.models import Instrument


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing orders.
    """
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['client', 'order_type', 'status', 'payment_status', 'order_date']
    search_fields = ['order_number', 'client__hospital_name', 'notes']
    ordering_fields = ['order_date', 'grand_total', 'created_at']
    ordering = ['-order_date']
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = Order.objects.all()
        
        if self.request.user.is_client:
            try:
                from clients.models import Client
                client = Client.objects.get(user=self.request.user)
                queryset = queryset.filter(client=client)
            except:
                return Order.objects.none()
        
        return queryset
    
    def perform_create(self, serializer):
        # Set created_by to current user
        serializer.save(created_by=self.request.user)
        
        # Update instrument status based on order type
        order = serializer.instance
        for item in order.items.all():
            instrument = item.instrument
            
            if order.order_type == 'sale':
                instrument.status = 'sold'
            elif order.order_type == 'rental':
                instrument.status = 'rented'
            elif order.order_type == 'storage':
                instrument.status = 'stored'
                
            instrument.save()
    
    @action(detail=True, methods=['post'])
    def generate_invoice(self, request, pk=None):
        """
        Generate an invoice for the order.
        """
        order = self.get_object()
        
        # Check if invoice already exists
        if hasattr(order, 'invoice'):
            return Response(
                {"detail": "Invoice already exists for this order."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get client's default billing address
        from clients.models import ClientAddress
        try:
            billing_address = ClientAddress.objects.filter(
                client=order.client,
                address_type__in=['billing', 'both'],
                is_default=True
            ).first()
            
            shipping_address = ClientAddress.objects.filter(
                client=order.client,
                address_type__in=['shipping', 'both'],
                is_default=True
            ).first()
            
            if not billing_address:
                return Response(
                    {"detail": "No billing address found for this client."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Format addresses
            billing_address_text = f"{billing_address.street_address}\n{billing_address.city}, {billing_address.state} {billing_address.postal_code}\n{billing_address.country}"
            
            shipping_address_text = None
            if shipping_address:
                shipping_address_text = f"{shipping_address.street_address}\n{shipping_address.city}, {shipping_address.state} {shipping_address.postal_code}\n{shipping_address.country}"
            
            # Create invoice
            due_date = timezone.now().date() + timezone.timedelta(days=30)  # Due in 30 days
            
            invoice = Invoice.objects.create(
                order=order,
                invoice_date=timezone.now().date(),
                due_date=due_date,
                status='draft',
                billing_address=billing_address_text,
                shipping_address=shipping_address_text if shipping_address_text else billing_address_text,
                terms_and_conditions="Payment is due within 30 days of invoice date. Late payments are subject to a 2% monthly interest charge."
            )
            
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {"detail": f"Error generating invoice: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel an order.
        """
        order = self.get_object()
        
        if order.status == 'completed':
            return Response(
                {"detail": "Cannot cancel a completed order."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update order status
        order.status = 'cancelled'
        order.save()
        
        # Update instrument status
        for item in order.items.all():
            instrument = item.instrument
            instrument.status = 'available'
            instrument.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing order items.
    """
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['order', 'instrument']
    search_fields = ['order__order_number', 'instrument__name', 'instrument__serial_number']
    
    def get_queryset(self):
        queryset = OrderItem.objects.all()
        
        if self.request.user.is_client:
            try:
                from clients.models import Client
                client = Client.objects.get(user=self.request.user)
                queryset = queryset.filter(order__client=client)
            except:
                return OrderItem.objects.none()
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing payments.
    """
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['order', 'payment_method', 'status', 'payment_date']
    search_fields = ['order__order_number', 'transaction_id', 'notes']
    ordering_fields = ['payment_date', 'amount', 'created_at']
    ordering = ['-payment_date']
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    def get_queryset(self):
        queryset = Payment.objects.all()
        
        if self.request.user.is_client:
            try:
                from clients.models import Client
                client = Client.objects.get(user=self.request.user)
                queryset = queryset.filter(order__client=client)
            except:
                return Payment.objects.none()
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Set created_by to current user
        serializer.save(created_by=self.request.user)
        
        # Update order payment status
        payment = serializer.instance
        order = payment.order
        
        # Calculate total paid amount
        total_paid = Payment.objects.filter(
            order=order,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Add current payment if it's completed
        if payment.status == 'completed':
            total_paid += payment.amount
        
        # Update order payment status
        if total_paid >= order.grand_total:
            order.payment_status = 'paid'
        elif total_paid > 0:
            order.payment_status = 'partial'
        else:
            order.payment_status = 'pending'
        
        order.save()
        
        # Update invoice status if it exists
        if hasattr(order, 'invoice'):
            invoice = order.invoice
            if order.payment_status == 'paid':
                invoice.status = 'paid'
                invoice.save()


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing invoices.
    """
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['order', 'status', 'invoice_date', 'due_date']
    search_fields = ['invoice_number', 'order__order_number', 'notes']
    ordering_fields = ['invoice_date', 'due_date', 'created_at']
    ordering = ['-invoice_date']
    
    def get_queryset(self):
        queryset = Invoice.objects.all()
        
        if self.request.user.is_client:
            try:
                from clients.models import Client
                client = Client.objects.get(user=self.request.user)
                queryset = queryset.filter(order__client=client)
            except:
                return Invoice.objects.none()
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """
        Mark invoice as sent.
        """
        invoice = self.get_object()
        invoice.status = 'sent'
        invoice.save()
        
        serializer = self.get_serializer(invoice)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """
        Mark invoice as paid.
        """
        invoice = self.get_object()
        invoice.status = 'paid'
        invoice.save()
        
        # Update order payment status
        order = invoice.order
        order.payment_status = 'paid'
        order.save()
        
        serializer = self.get_serializer(invoice)
        return Response(serializer.data)
