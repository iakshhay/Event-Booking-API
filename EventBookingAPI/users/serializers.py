from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User,Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','first_name','last_name','role','created_at','updated_at']
        extra_kwargs={
            'role':{'read_only':True},
            'created_at':{'read_only':True},
            'updated_at':{'read_only':True},
        }

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8,required=True)
    password_confirmation=serializers.CharField(write_only=True,min_length=8,required=True)

    class Meta:
        model=User 
        fields=['username','email','first_name','last_name','password','password_confirmation']
        
    def validate_email(self,value):
        value=value.strip().lower()
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already taken.")
        return value
    
    def validate(self,data):
        if data['password']!=data['password_confirmation']:
            raise ValidationError("Passwords do not match.")
        return data

    def create(self,validated_data):
        validated_data.pop('password_confirmation')
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Profile
        fields="__all__"
        