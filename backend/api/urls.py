from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('items', views.ItemViewSet, basename="items")



urlpatterns = router.urls

