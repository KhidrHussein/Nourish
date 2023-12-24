from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('api/customusers/', include(router.urls)),
    # Add other URL patterns as needed
]

urlpatterns += [
    path('customusers/sign_up/', CustomUserViewSet.as_view({'post': 'sign_up'}), name='sign_up'),
    path('customusers/register/', CustomUserViewSet.as_view({'post': 'register'}), name='register'),
    path('customusers/log_in/', CustomUserViewSet.as_view({'post': 'log_in'}), name='log_in'),
]