from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)

urlpatterns = [
    
]

urlpatterns += router.urls
