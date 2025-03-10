from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client, ClientContact, ClientAddress
from .serializers import (
    ClientSerializer, ClientDetailSerializer, ClientCreateSerializer,
    ClientContactSerializer, ClientAddressSerializer
)
from accounts.permissions import IsAdminUser, IsStaffUser, IsClientUser


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing clients.
    """
    queryset = Client.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hospital_type', 'is_active']
    search_fields = ['hospital_name', 'registration_number', 'tax_id']
    ordering_fields = ['hospital_name', 'created_at']
    ordering = ['hospital_name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ClientCreateSerializer
        elif self.action in ['retrieve', 'me']:
            return ClientDetailSerializer
        return ClientSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action == 'me':
            permission_classes = [IsClientUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get the client profile of the authenticated user.
        """
        try:
            client = Client.objects.get(user=request.user)
            serializer = self.get_serializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response(
                {"detail": "Client profile not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )


class ClientContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing client contacts.
    """
    serializer_class = ClientContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['client', 'is_primary']
    search_fields = ['name', 'email', 'phone']
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return ClientContact.objects.all()
        elif self.request.user.is_staff_member:
            return ClientContact.objects.all()
        elif self.request.user.is_client:
            try:
                client = Client.objects.get(user=self.request.user)
                return ClientContact.objects.filter(client=client)
            except Client.DoesNotExist:
                return ClientContact.objects.none()
        return ClientContact.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]


class ClientAddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing client addresses.
    """
    serializer_class = ClientAddressSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['client', 'address_type', 'is_default']
    search_fields = ['street_address', 'city', 'state', 'postal_code']
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return ClientAddress.objects.all()
        elif self.request.user.is_staff_member:
            return ClientAddress.objects.all()
        elif self.request.user.is_client:
            try:
                client = Client.objects.get(user=self.request.user)
                return ClientAddress.objects.filter(client=client)
            except Client.DoesNotExist:
                return ClientAddress.objects.none()
        return ClientAddress.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]
