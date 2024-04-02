from rest_framework import serializers
from .models import UserModel


class UserRegistrationSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = UserModel
        # Define fields for registration serializer
        fields = ['name','phone','password','email']
        extra_kwargs = {
            'password': {'write_only': True},  
              
        }

    # Create user instance
    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)