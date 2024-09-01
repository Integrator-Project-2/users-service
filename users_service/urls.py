from django.contrib import admin
from django.urls import path, include
from authentication.views import CustomTokenObtainPairView, GoogleCallbackView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pacients.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('doctors.urls')),

    path('api/auth/', include('allauth.urls')),
    # path('api/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/auth/google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    
]