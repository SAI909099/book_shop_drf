from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import UserListAPIView, UpdateUserView, RegisterCreateAPIView, LoginAPIView, CustomTokenObtainPairView

urlpatterns = [
    path('user/', UserListAPIView.as_view()),
    path('update-user/', UpdateUserView.as_view(), name='update-user'),

    path('auth/register', RegisterCreateAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),

    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
]