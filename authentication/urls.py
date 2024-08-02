from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    AuthenticationViewSet,
)

urlpatterns = [
    path('register/', AuthenticationViewSet.as_view({'post': 'register'})),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
]
