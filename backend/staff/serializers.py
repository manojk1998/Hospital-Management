from rest_framework import serializers
from .models import StaffDepartment, StaffMember, Attendance, Leave
from accounts.serializers import UserSerializer


class StaffDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffDepartment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class StaffMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = StaffMember
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class StaffMemberDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department = StaffDepartmentSerializer(read_only=True)
    
    class Meta:
        model = StaffMember
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class StaffMemberCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = StaffMember
        exclude = ('user',)
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        # Extract user data
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        
        # Create user with staff role
        from accounts.models import User
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='staff'
        )
        
        # Create staff profile
        staff_member = StaffMember.objects.create(user=user, **validated_data)
        return staff_member


class AttendanceSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.user.full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class LeaveSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.user.full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.full_name', read_only=True)
    
    class Meta:
        model = Leave
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class LeaveApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ('status', 'rejection_reason')
        
    def validate(self, data):
        if data.get('status') == 'rejected' and not data.get('rejection_reason'):
            raise serializers.ValidationError("Rejection reason is required when rejecting a leave request.")
        return data 