from rest_framework import serializers
from .models import Order, OrderItem, Payment, Invoice
from accounts.serializers import UserSerializer
from clients.serializers import ClientSerializer
from instruments.serializers import InstrumentSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    instrument_details = InstrumentSerializer(source='instrument', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('subtotal', 'created_at', 'updated_at')


class PaymentSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('invoice_number', 'created_at', 'updated_at')


class OrderSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_number', 'grand_total', 'created_at', 'updated_at')


class OrderDetailSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    invoice = InvoiceSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_number', 'grand_total', 'created_at', 'updated_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_number', 'grand_total', 'created_at', 'updated_at', 'created_by')
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calculate total amount from items
        total_amount = sum(item.get('unit_price', 0) * item.get('quantity', 1) for item in items_data)
        
        # For rental items, multiply by duration
        for item in items_data:
            if validated_data.get('order_type') == 'rental' and item.get('rental_duration_days'):
                total_amount += item.get('unit_price', 0) * item.get('quantity', 1) * item.get('rental_duration_days')
        
        validated_data['total_amount'] = total_amount
        
        # Create order
        order = Order.objects.create(**validated_data)
        
        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order
    
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        
        # Update order fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if items_data is not None:
            # Delete existing items
            instance.items.all().delete()
            
            # Create new items
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
            
            # Recalculate total amount
            total_amount = sum(item.get('unit_price', 0) * item.get('quantity', 1) for item in items_data)
            
            # For rental items, multiply by duration
            for item in items_data:
                if instance.order_type == 'rental' and item.get('rental_duration_days'):
                    total_amount += item.get('unit_price', 0) * item.get('quantity', 1) * item.get('rental_duration_days')
            
            instance.total_amount = total_amount
        
        instance.save()
        return instance


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')


class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('invoice_number', 'created_at', 'updated_at') 