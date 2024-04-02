from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from fuzzywuzzy import process,fuzz
from user.models import Movie
from .serializers import MovieSerializer, UserLoginSerializer, UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#generate token manaually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({ 'token': token,'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Registration Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)
    


class UserLogin(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    

class AddMovieAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, format=None):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)  # the 'user' field auto filled with logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class MovieListAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        movie_count = movies.count()
        data = {
            'total_movie': movie_count,
            'movies': serializer.data
        }
        return Response(data)
    

class MovieSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        query_params = request.query_params
        name = query_params.get('name')
        if not name:
            return Response({"error": "Please provide a name for search."}, status=status.HTTP_400_BAD_REQUEST)
        movies = Movie.objects.all()
         # Fuzzy matching partially near result by name
        try:
            movie_names = [movie.name for movie in movies]
            name_match = process.extractOne(name, movie_names, scorer=fuzz.token_sort_ratio)
            if name_match[1] > 80: 
                movies = movies.filter(name=name_match[0])
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = MovieSerializer(movies, many=True)
        movie_count = movies.count()
        response_data = {
            'count': movie_count,
            'movies': serializer.data
        }
        return Response(response_data)