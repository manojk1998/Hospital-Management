from django.contrib import admin
from .models import StaffDepartment, StaffMember, Attendance, Leave


@admin.register(StaffDepartment)
class StaffDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    max_num = 10
    readonly_fields = ('created_at', 'updated_at')


class LeaveInline(admin.TabularInline):
    model = Leave
    extra = 0
    max_num = 5
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'role', 'date_of_joining', 'is_active')
    list_filter = ('department', 'role', 'is_active', 'date_of_joining')
    search_fields = ('employee_id', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AttendanceInline, LeaveInline]
    fieldsets = (
        (None, {
            'fields': ('user', 'employee_id', 'department', 'role')
        }),
        ('Employment Details', {
            'fields': ('date_of_joining', 'salary', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('emergency_contact_name', 'emergency_contact_number', 'address')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'status', 'check_in_time', 'check_out_time')
    list_filter = ('status', 'date')
    search_fields = ('staff__employee_id', 'staff__user__email', 'staff__user__first_name', 'staff__user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('staff', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by')
    list_filter = ('leave_type', 'status', 'start_date')
    search_fields = ('staff__employee_id', 'staff__user__email', 'staff__user__first_name', 'staff__user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'start_date'
    fieldsets = (
        (None, {
            'fields': ('staff', 'leave_type', 'start_date', 'end_date', 'reason')
        }),
        ('Approval Details', {
            'fields': ('status', 'approved_by', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
