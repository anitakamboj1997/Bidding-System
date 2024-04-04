from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from authentication.models import CustomUser
from rest_framework.permissions import IsAuthenticated

class UserRegistrationAPIView(APIView):
    def post(self, request):
        resp = {}
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resp["message"] = "User Credated Successfully"
            resp["status"] = status.HTTP_201_CREATED
            resp["data"] = serializer.data
            return Response(resp, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request, format=None):
        resp = {}
        print(request.user.username)
        profile = CustomUser.objects.get(username=request.user.username)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            resp["message"] = "User Updated Successfully"
            resp["status"] = status.HTTP_200_OK
            resp["data"] = serializer.data
            return Response(resp, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]