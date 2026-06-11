from rest_framework.routers import DefaultRouter
from .views import MonthlyStatistics

router = DefaultRouter()
router.register("statics", MonthlyStatistics, basename="statics")

urlpatterns = router.urls
