from django.contrib import admin
from .models import Report, Dashboard, Widget


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'format', 'created_by', 'created_at')
    list_filter = ('report_type', 'format', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'report_type', 'description')
        }),
        ('Parameters', {
            'fields': ('parameters', 'start_date', 'end_date', 'format')
        }),
        ('File', {
            'fields': ('file',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )


class WidgetInline(admin.TabularInline):
    model = Widget
    extra = 1
    fields = ('title', 'widget_type', 'chart_type', 'data_source', 'position_x', 'position_y', 'width', 'height')


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'created_by', 'created_at')
    list_filter = ('is_default', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [WidgetInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_default')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'dashboard', 'widget_type', 'chart_type', 'position_x', 'position_y')
    list_filter = ('widget_type', 'chart_type', 'dashboard')
    search_fields = ('title', 'data_source')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('dashboard', 'title', 'widget_type', 'chart_type')
        }),
        ('Data', {
            'fields': ('data_source', 'query_parameters')
        }),
        ('Layout', {
            'fields': ('position_x', 'position_y', 'width', 'height')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
