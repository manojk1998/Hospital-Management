from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import datetime, timedelta
from .models import StaffDepartment, StaffMember, Attendance, Leave
from .serializers import (
    StaffDepartmentSerializer, StaffMemberSerializer, StaffMemberDetailSerializer,
    StaffMemberCreateSerializer, AttendanceSerializer, LeaveSerializer, LeaveApprovalSerializer
)
from accounts.permissions import IsAdminUser, IsStaffUser


class StaffDepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing staff departments.
    """
    queryset = StaffDepartment.objects.all()
    serializer_class = StaffDepartmentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class StaffMemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing staff members.
    """
    queryset = StaffMember.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'role', 'is_active']
    search_fields = ['employee_id', 'user__email', 'user__first_name', 'user__last_name']
    ordering_fields = ['employee_id', 'date_of_joining', 'created_at']
    ordering = ['employee_id']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StaffMemberCreateSerializer
        elif self.action in ['retrieve', 'me']:
            return StaffMemberDetailSerializer
        return StaffMemberSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action == 'me':
            permission_classes = [IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get the staff profile of the authenticated user.
        """
        try:
            staff = StaffMember.objects.get(user=request.user)
            serializer = self.get_serializer(staff)
            return Response(serializer.data)
        except StaffMember.DoesNotExist:
            return Response(
                {"detail": "Staff profile not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing staff attendance.
    """
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['staff', 'date', 'status']
    search_fields = ['staff__employee_id', 'staff__user__first_name', 'staff__user__last_name']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Attendance.objects.all()
        elif self.request.user.is_staff_member:
            try:
                staff = StaffMember.objects.get(user=self.request.user)
                return Attendance.objects.filter(staff=staff)
            except StaffMember.DoesNotExist:
                return Attendance.objects.none()
        return Attendance.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'])
    def check_in(self, request):
        """
        Record staff check-in for today.
        """
        try:
            staff = StaffMember.objects.get(user=request.user)
            today = timezone.now().date()
            
            # Check if attendance record already exists for today
            attendance, created = Attendance.objects.get_or_create(
                staff=staff,
                date=today,
                defaults={
                    'status': 'present',
                    'check_in_time': timezone.now().time()
                }
            )
            
            if not created:
                if attendance.check_in_time:
                    return Response(
                        {"detail": "You have already checked in today."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                attendance.status = 'present'
                attendance.check_in_time = timezone.now().time()
                attendance.save()
            
            serializer = self.get_serializer(attendance)
            return Response(serializer.data)
        except StaffMember.DoesNotExist:
            return Response(
                {"detail": "Staff profile not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def check_out(self, request):
        """
        Record staff check-out for today.
        """
        try:
            staff = StaffMember.objects.get(user=request.user)
            today = timezone.now().date()
            
            try:
                attendance = Attendance.objects.get(staff=staff, date=today)
                
                if not attendance.check_in_time:
                    return Response(
                        {"detail": "You need to check in first."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if attendance.check_out_time:
                    return Response(
                        {"detail": "You have already checked out today."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                attendance.check_out_time = timezone.now().time()
                attendance.save()
                
                serializer = self.get_serializer(attendance)
                return Response(serializer.data)
            except Attendance.DoesNotExist:
                return Response(
                    {"detail": "No check-in record found for today."},
                    status=status.HTTP_404_NOT_FOUND
                )
        except StaffMember.DoesNotExist:
            return Response(
                {"detail": "Staff profile not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )


class LeaveViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing staff leave requests.
    """
    serializer_class = LeaveSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['staff', 'leave_type', 'status', 'start_date']
    search_fields = ['staff__employee_id', 'staff__user__first_name', 'staff__user__last_name']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-start_date']
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Leave.objects.all()
        elif self.request.user.is_staff_member:
            try:
                staff = StaffMember.objects.get(user=self.request.user)
                return Leave.objects.filter(staff=staff)
            except StaffMember.DoesNotExist:
                return Leave.objects.none()
        return Leave.objects.none()
    
    def get_permissions(self):
        if self.action in ['approve', 'reject']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsStaffUser]
        else:
            permission_classes = [IsAdminUser | IsStaffUser]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        if self.request.user.is_staff_member:
            try:
                staff = StaffMember.objects.get(user=self.request.user)
                serializer.save(staff=staff)
            except StaffMember.DoesNotExist:
                raise serializers.ValidationError("Staff profile not found for this user.")
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve a leave request.
        """
        leave = self.get_object()
        serializer = LeaveApprovalSerializer(leave, data={'status': 'approved'}, partial=True)
        
        if serializer.is_valid():
            serializer.save(approved_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject a leave request.
        """
        leave = self.get_object()
        serializer = LeaveApprovalSerializer(leave, data={
            'status': 'rejected',
            'rejection_reason': request.data.get('rejection_reason', '')
        }, partial=True)
        
        if serializer.is_valid():
            serializer.save(approved_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
