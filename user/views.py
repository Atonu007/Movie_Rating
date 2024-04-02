from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.db.models import Avg 
from fuzzywuzzy import process,fuzz
from user.models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserLoginSerializer, UserRegistrationSerializer


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
            movie = serializer.save(user=self.request.user)
            average_rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
            movie_data = {
                'id': movie.id,
                'name': movie.name,
                'genre': movie.genre,
                'rating': average_rating,
                'release_date': movie.release_date.strftime('%m-%d-%Y'),  
            }
            return Response(movie_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class MovieListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        movies = Movie.objects.all()
        movies_count = movies.count()
        serialized_data = []

        for movie in movies:
            average_rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
            if average_rating is None:
                average_rating = 0.0

            movie_data = {
                'id': movie.id,
                'name': movie.name,
                'genre': movie.genre,
                'release_date': movie.release_date,
                'rating': average_rating,
            }
            serialized_data.append(movie_data)

        return Response(
            {
            "count": movies_count,
            "data": serialized_data,
            }
            , status=status.HTTP_200_OK
            )
    

class MovieSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query_params = request.query_params
        name = query_params.get('name')
        serialized_data =[]

        if not name:
            return Response({"error": "Please provide a name for search."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movies = Movie.objects.filter(name__icontains=name) 

            # Fuzzy matching for partial matches 
            if request.query_params.get('fuzzy', False):
                
                movie_names = [movie.name for movie in movies]
                high_match = process.extractOne(name, movie_names, scorer=fuzz.token_sort_ratio, score_cutoff=80)
                if high_match:
                    movies = movies.filter(name=high_match[0])

            movies_count = movies.count()
            serialized_data = []
            for movie in movies:
                average_rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
                if average_rating is None:
                    average_rating = 0.0

                movie_data = {
                    'id': movie.id,
                    'name': movie.name,
                    'genre': movie.genre,
                    'release_date': movie.release_date,
                    'rating': average_rating,
                }
                serialized_data.append(movie_data)

            return Response({
                "count": movies_count,
                "data": serialized_data,
            })

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class RateMovieAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id, format=None):
        user = self.request.user
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid():
            rating_value = serializer.validated_data['rating']
            if Rating.objects.filter(user=user, movie=movie).exists():
                return Response({'error': 'You have already rated this movie'}, status=status.HTTP_400_BAD_REQUEST)

            rating = Rating(user=user, movie=movie, rating=rating_value)
            rating.save()

            rating_data = {
                "id": rating.id,
                "user_id": user.id,
                "movie_id": movie.id,
                "rating": rating_value
            }

            return Response(rating_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)