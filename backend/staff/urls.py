from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffDepartmentViewSet, StaffMemberViewSet, AttendanceViewSet, LeaveViewSet

router = DefaultRouter()
router.register(r'departments', StaffDepartmentViewSet, basename='staff-department')
router.register(r'members', StaffMemberViewSet, basename='staff-member')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'leaves', LeaveViewSet, basename='leave')

urlpatterns = [
    path('', include(router.urls)),
] 