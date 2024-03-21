from rest_framework.routers import DefaultRouter
from .views import PacientViewSet

router = DefaultRouter()
router.register(r'pacients', PacientViewSet)


urlpatterns = [

]

urlpatterns += router.urls
