from rest_framework.routers import DefaultRouter
from .views import PacientViewSet   
from django.urls import path, include

router = DefaultRouter()
router.register(r'pacients', PacientViewSet)


urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += router.urls
