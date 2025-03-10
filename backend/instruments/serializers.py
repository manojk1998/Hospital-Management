from rest_framework import serializers
from .models import InstrumentCategory, Instrument, InstrumentMaintenance


class InstrumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentCategory
        fields = '__all__'


class InstrumentMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentMaintenance
        fields = '__all__'


class InstrumentSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    qr_code_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Instrument
        fields = '__all__'
        extra_fields = ['category_name', 'qr_code_url']
    
    def get_qr_code_url(self, obj):
        if obj.qr_code:
            return self.context['request'].build_absolute_uri(obj.qr_code.url)
        return None


class InstrumentDetailSerializer(serializers.ModelSerializer):
    category = InstrumentCategorySerializer(read_only=True)
    maintenance_records = InstrumentMaintenanceSerializer(many=True, read_only=True)
    qr_code_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Instrument
        fields = '__all__'
        extra_fields = ['maintenance_records', 'qr_code_url']
    
    def get_qr_code_url(self, obj):
        if obj.qr_code:
            return self.context['request'].build_absolute_uri(obj.qr_code.url)
        return None 