from rest_framework import serializers
from .models import Client, ClientContact, ClientAddress
from accounts.serializers import UserSerializer


class ClientAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAddress
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ClientContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientContact
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    contacts = ClientContactSerializer(many=True, read_only=True)
    addresses = ClientAddressSerializer(many=True, read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ClientDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    contacts = ClientContactSerializer(many=True, read_only=True)
    addresses = ClientAddressSerializer(many=True, read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ClientCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Client
        exclude = ('user',)
        read_only_fields = ('created_at', 'updated_at')
    
    def create(self, validated_data):
        # Extract user data
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        
        # Create user with client role
        from accounts.models import User
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='client'
        )
        
        # Create client profile
        client = Client.objects.create(user=user, **validated_data)
        return client 