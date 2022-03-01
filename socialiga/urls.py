"""socialiga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from django.views.generic import RedirectView, TemplateView

from analytics.views import SalesView, SalesAjaxView
from carts.api.views import cart_detail_api_view
from orders.api.views import LibraryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(('accounts.api.urls', 'api-auth'), namespace='api-auth')),
    path('api/user/', include(('accounts.api.user.urls', 'api-user'), namespace='api-user')),
    path('api/billing/', include(('billing.api.urls', 'api-billing'), namespace='api-billing')),
    path('api/blog/', include(('blog.api.urls', 'api-blog'), namespace='api-blog')),
    path('api/events/', include(('event.api.urls', 'api-events'), namespace='api-events')),
    path('api/products/', include(('products.api.urls', 'api-products'), namespace='api-products')),
    path('api/order/', include(('orders.api.urls', 'api-order'), namespace='api-order')),
    path('api/analytics/sales/', SalesView.as_view(), name='sales-analytics'),
    path('api/analytics/sales/data/', SalesAjaxView.as_view(), name='sales-analytics-data'),
    # path('api/checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    # path('api/checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('api/cart/info/', include(('carts.api.urls', 'api-cart'), namespace='api-cart')),
    # path('api/billing/payment-method/', payment_method_view, name='billing-payment-method'),
    # path('api/billing/payment-method/create/', payment_method_createview, name='billing-payment-method-endpoint'),
    path('api/library/', LibraryView.as_view(), name='library'),
]

# authentication urls
urlpatterns += [
    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include(('accounts.urls', 'account-url'), namespace='account-url')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# url to catch any unmatched url used for 404 error
urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='404.html'))]
