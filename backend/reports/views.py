from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from django.http import HttpResponse
import io
from .models import Report, Dashboard, Widget
from .serializers import (
    ReportSerializer, DashboardSerializer, DashboardDetailSerializer,
    WidgetSerializer, ReportGenerateSerializer, WidgetDataSerializer
)
from accounts.permissions import IsAdminUser, IsStaffUser, IsClientUser


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing reports.
    """
    queryset = Report.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'format', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    serializer_class = ReportSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'generate']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download a report file.
        """
        report = self.get_object()
        
        if not report.file:
            return Response(
                {"detail": "No file available for this report."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Return the file
        response = HttpResponse(report.file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{report.file.name}"'
        return response


class DashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing dashboards.
    """
    queryset = Dashboard.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_default', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-is_default', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DashboardDetailSerializer
        return DashboardSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def default(self, request):
        """
        Get the default dashboard.
        """
        dashboard = Dashboard.objects.filter(is_default=True).first()
        
        if not dashboard:
            return Response(
                {"detail": "No default dashboard found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = DashboardDetailSerializer(dashboard)
        return Response(serializer.data)


class WidgetViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing dashboard widgets.
    """
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['dashboard', 'widget_type', 'chart_type']
    search_fields = ['title', 'data_source']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser | IsClientUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):
        """
        Get data for a widget.
        """
        widget = self.get_object()
        
        # Parse parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Generate widget data
        data = {
            'title': widget.title,
            'type': widget.widget_type,
            'chart_type': widget.chart_type,
            'data': {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'datasets': [{
                    'label': 'Sample Data',
                    'data': [12, 19, 3, 5, 2, 3]
                }]
            }
        }
        
        return Response(data) 