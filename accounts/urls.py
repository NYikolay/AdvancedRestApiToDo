from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import CreateUser, CookieTokenObtainPairView, CookieTokenRefreshView

urlpatterns = [
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),

    path('registrer/', CreateUser.as_view(), name='registration')
]
