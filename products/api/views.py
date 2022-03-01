from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart

from products.api.mixins import IsVendor
from products.api.serializers import ProductSerializer
from products.models import Product


class ProductCreateAPIView(IsVendor, CreateAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_class = IsAuthenticated
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.partial = True
        serializer.save(user=self.request.user)


class ProductFeaturedListAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_class = IsAuthenticated
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedRetrieveAPIView(ObjectViewedMixin, RetrieveAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_class = IsAuthenticated
    serializer_class = ProductSerializer
    queryset = Product.objects.all().featured()
    lookup_field = 'slug'


class UserProductHistoryAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_class = IsAuthenticated
    serializer_class = ProductSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super(UserProductHistoryAPIView, self).get_serializer_context(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return request.user.objectviewed_set.by_model(Product, model_queryset=False)


class ProductListAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_class = IsAuthenticated
    serializer_class = ProductSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super(ProductListAPIView, self).get_serializer_context(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


class ProductDetailSlugAPIView(ObjectViewedMixin, RetrieveAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_class = IsAuthenticated
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(ProductDetailSlugAPIView, self).get_serializer_context(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            return Response({'message': 'An error has occurred'}, status=status.HTTP_200_OK)
        return instance
