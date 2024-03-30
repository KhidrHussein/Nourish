from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Payment, NewsletterSubscription, Cart


# Register your models here.

# admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(NewsletterSubscription)
admin.site.register(Cart)
