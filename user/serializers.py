from rest_framework import serializers
from .models import Movie, Rating, UserModel
from django.db.models import Avg 


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['name','phone','password','email']
        extra_kwargs = {
            'password': {'write_only': True},  
            }
    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)  
    
    class Meta:
        model = UserModel
        fields = ['email', 'password']

    
class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()  

    def get_average_rating(self, obj):
        average_rating = obj.ratings.aggregate(Avg('rating'))['rating__avg']
        return average_rating if average_rating else 0  

    class Meta:
        model = Movie
        exclude = ('user',)


class RatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)  

    class Meta:
        model = Rating
        fields = ('id', 'user_id', 'movie_id', 'rating', 'user_name', 'created_at')
