from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ClientContactViewSet, ClientAddressViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'contacts', ClientContactViewSet, basename='client-contact')
router.register(r'addresses', ClientAddressViewSet, basename='client-address')

urlpatterns = [
    path('', include(router.urls)),
] 