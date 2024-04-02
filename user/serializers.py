from rest_framework import serializers
from .models import UserModel



#user registration
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
    

#user login
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)  
    
    class Meta:
        model = UserModel
        fields = ['email', 'password']

    
