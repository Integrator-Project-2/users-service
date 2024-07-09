from django.contrib import admin
from django.urls import path, include
from authentication.views import CompleteProfileView, CustomTokenObtainPairView, GoogleCallbackView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pacients.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('doctors.urls')),

    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/', include('allauth.urls')),
    # path('api/google/', GoogleLogin.as_view(), name='google_login'),
    path('complete-profile/', CompleteProfileView.as_view(), name='complete_profile'),
    path('api/auth/google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
    
]