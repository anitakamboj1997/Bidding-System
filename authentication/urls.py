from django.urls import path
from .views import UserRegistrationAPIView, MyTokenObtainPairView, UpdateProfileView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register_user'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),
] 