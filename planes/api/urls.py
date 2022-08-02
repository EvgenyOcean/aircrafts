from rest_framework.routers import DefaultRouter

from .views import SeriesViewSet, PlaneViewSet


router = DefaultRouter()
router.register("series", SeriesViewSet)
router.register("planes", PlaneViewSet)


urlpatterns = [
    *router.urls
]