from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, OrderViewSet, OrderItemViewSet, ProductViewSet, PaymentViewSet, NewsletterSubscriptionViewSet, CartViewSet


router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'order-item', OrderItemViewSet, basename='order-item')
router.register(r'product', ProductViewSet, basename='product')
# router.register(r'payment', PaymentViewSet, basename='payment')
router.register(r'newsletter-subscription', NewsletterSubscriptionViewSet, basename='newsletter-subscription')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'paystack-payments', PaymentViewSet, basename='paystack-payments')


urlpatterns = [
    path('api/base/', include(router.urls)),
    path('', views.home,  name="home"),
    path('paystack-webhook', views.paystack_webhook,  name="paystack_webhook"),

    # path('login', views.log_in, name="login"),
    # path('sign_up', views.sign_up, name="sign_up"),
    # path('register', views.register, name="register"),
]