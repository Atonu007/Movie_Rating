from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer


# Create your views here.


class UserRegistration(APIView):
   
    #API endpoint for user registration.
   
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
           
            return Response({ 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Registration Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)