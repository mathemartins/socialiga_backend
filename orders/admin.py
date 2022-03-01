from django.contrib import admin

from orders.models import Order, ProductPurchase

admin.site.register(Order)
admin.site.register(ProductPurchase)