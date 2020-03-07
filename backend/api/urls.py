from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('items', views.ItemViewSet, basename="items")
router.register('containers', views.ContainerViewSet, basename="containers")
router.register('spawns', views.SpawnViewSet, basename="spawns")

urlpatterns = router.urls

