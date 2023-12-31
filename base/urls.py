from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, OrderViewSet, OrderItemViewSet, ProductViewSet, PaymentViewSet, NewsletterSubscriptionViewSet


router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'order-item', OrderItemViewSet, basename='order-item')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'payment', PaymentViewSet, basename='payment')
router.register(r'newsletter-subscription', NewsletterSubscriptionViewSet, basename='newsletter-subscription')


urlpatterns = [
    path('api/base/', include(router.urls)),
    path('', views.home,  name="home"),

    # path('login', views.log_in, name="login"),
    # path('sign_up', views.sign_up, name="sign_up"),
    # path('register', views.register, name="register"),
]