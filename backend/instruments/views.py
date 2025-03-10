from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
import qrcode
from io import BytesIO

from .models import InstrumentCategory, Instrument, InstrumentMaintenance
from .serializers import (
    InstrumentCategorySerializer, InstrumentSerializer, 
    InstrumentDetailSerializer, InstrumentMaintenanceSerializer
)
from accounts.permissions import IsAdminOrStaff, IsAdminOrStaffOrReadOnly


class InstrumentCategoryViewSet(viewsets.ModelViewSet):
    queryset = InstrumentCategory.objects.all()
    serializer_class = InstrumentCategorySerializer
    permission_classes = [IsAdminOrStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    permission_classes = [IsAdminOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['name', 'serial_number', 'description', 'manufacturer']
    ordering_fields = ['name', 'purchase_date', 'purchase_price', 'rental_price_per_day', 'selling_price']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InstrumentDetailSerializer
        return InstrumentSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    @action(detail=True, methods=['get'])
    def qr_code(self, request, pk=None):
        """Generate and return a QR code for the instrument."""
        instrument = self.get_object()
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"Instrument: {instrument.name}\nSerial: {instrument.serial_number}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        return HttpResponse(buffer, content_type="image/png")
    
    @action(detail=True, methods=['get'])
    def maintenance_history(self, request, pk=None):
        """Get maintenance history for an instrument."""
        instrument = self.get_object()
        maintenance_records = instrument.maintenance_records.all()
        serializer = InstrumentMaintenanceSerializer(maintenance_records, many=True)
        return Response(serializer.data)


class InstrumentMaintenanceViewSet(viewsets.ModelViewSet):
    queryset = InstrumentMaintenance.objects.all()
    serializer_class = InstrumentMaintenanceSerializer
    permission_classes = [IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['instrument', 'maintenance_date']
    search_fields = ['description', 'performed_by']
    ordering_fields = ['maintenance_date', 'next_maintenance_date', 'cost']
