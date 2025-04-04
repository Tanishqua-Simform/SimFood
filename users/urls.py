from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterView, TestingAuth

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/protected/', TestingAuth.as_view(), name='protected'),
]
