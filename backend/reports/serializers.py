from rest_framework import serializers
from .models import Report, Dashboard, Widget
from accounts.serializers import UserSerializer


class ReportSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'file')


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class DashboardSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Dashboard
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class DashboardDetailSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    widgets = WidgetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dashboard
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ReportGenerateSerializer(serializers.Serializer):
    report_type = serializers.ChoiceField(choices=Report.REPORT_TYPES)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    format = serializers.ChoiceField(choices=Report.FORMAT_CHOICES, default='pdf')
    parameters = serializers.JSONField(required=False)


class WidgetDataSerializer(serializers.Serializer):
    dashboard_id = serializers.IntegerField()
    widget_id = serializers.IntegerField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    parameters = serializers.JSONField(required=False) 