from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstrumentViewSet, InstrumentCategoryViewSet, InstrumentMaintenanceViewSet

router = DefaultRouter()
router.register(r'instruments', InstrumentViewSet, basename='instrument')
router.register(r'categories', InstrumentCategoryViewSet, basename='instrument-category')
router.register(r'maintenance', InstrumentMaintenanceViewSet, basename='instrument-maintenance')

urlpatterns = [
    path('', include(router.urls)),
] 