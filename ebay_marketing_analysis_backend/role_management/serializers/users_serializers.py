from rest_framework import serializers
from role_management.models import CustomUser, Role
from django.contrib.auth import authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', read_only=True)  

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'role', 'phone_number']
           

class CustomRegisterSerializer(serializers.ModelSerializer):
    
    email=serializers.EmailField(required=False) 
    name=serializers.CharField(required=False)
    role = serializers.CharField(max_length=35) 
    phone_number=serializers.CharField(max_length=13, required=False)
    password=serializers.CharField(write_only=False, required=False)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'role', 'phone_number', 'password']
        
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_field(self, value):
        if not CustomUser.objects.all().values('name').exists():
            raise serializers.ValidationError("Name Field Required.")
        elif CustomUser.objects.all().values('phone_number').exists() is None:
            raise serializers.ValidationError("PhoneNumber Field Required.")
        elif CustomUser.objects.all().values('role').exists() is None:
            raise serializers.ValidationError("Role Field Required.")
        return value
    
    def create(self, validated_data):
        role_data = validated_data.pop('role')
        try:
            if isinstance(role_data, str):
                role = Role.objects.get(name=role_data)
            else:
                role = Role.objects.get(id=role_data)
        except Role.DoesNotExist:
            raise serializers.ValidationError('Role not found')
      
        
        user= CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            role=role
        )                              
        user.set_password(validated_data['password'])
       
        user.save()
        return user
        
    def update(self, instance, validated_data):
        # Perform partial update by updating only the fields provided in validated_data
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
        

            

        

        
