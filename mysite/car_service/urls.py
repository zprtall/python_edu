from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, WorkshopViewSet, WorkerViewSet

router = DefaultRouter()
router.register("companies", CompanyViewSet, basename="company")
router.register("workshops", WorkshopViewSet, basename="workshop")
router.register("workers", WorkerViewSet, basename="worker")

urlpatterns = router.urls
