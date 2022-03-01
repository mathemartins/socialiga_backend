from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from billing.models import BillingProfile
from .serializers import UserDetailSerializer
from ...models import Address

User = get_user_model()


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    lookup_field = 'username'  # id

    def get_serializer_context(self):
        return {'request': self.request}


class UserAddressAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, *args, **kwargs):
        address = Address.objects.create(
            user=self.request.user,
            name=self.kwargs.get('name'),
            street=self.kwargs.get('street'),
            locale=self.kwargs.get('locale'),
            zip_code=self.kwargs.get('zipCode'),
            state=self.kwargs.get('state')
        )
        return Response(
            {'message': '{address_name} has been created successfully!'.format(address_name=address.name)},
            status=201
        )

    def get(self, request, *args, **kwargs):
        # returns serialize list of user array
        print(self.request.user)
        qs = Address.objects.filter(user=self.request.user).values()
        return Response(qs, status=200)


# def checkout_address_create_view(request):
#     billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
#     if billing_profile is not None:
#         address_type = request.POST.get('address_type', 'shipping')
#         instance.billing_profile = billing_profile
#         instance.address_type = address_type
#         instance.save()
#         request.session[address_type + "_address_id"] = instance.id
#         print(address_type + "_address_id")
#     else:
#         print("Error here")
#         return redirect("cart:checkout")
#     form = AddressCheckoutForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         print(request.POST)
#         instance = form.save(commit=False)
#         billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
#         if billing_profile is not None:
#             address_type = request.POST.get('address_type', 'shipping')
#             instance.billing_profile = billing_profile
#             instance.address_type = address_type
#             instance.save()
#             request.session[address_type + "_address_id"] = instance.id
#             print(address_type + "_address_id")
#         else:
#             print("Error here")
#             return redirect("cart:checkout")
#
#         if is_safe_url(redirect_path, request.get_host()):
#             return redirect(redirect_path)
#     return redirect("cart:checkout")
#
#
# def checkout_address_reuse_view(request):
#     if request.user.is_authenticated():
#         context = {}
#         next_ = request.GET.get('next')
#         next_post = request.POST.get('next')
#         redirect_path = next_ or next_post or None
#         if request.method == "POST":
#             print(request.POST)
#             shipping_address = request.POST.get('shipping_address', None)
#             address_type = request.POST.get('address_type', 'shipping')
#             billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
#             if shipping_address is not None:
#                 qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
#                 if qs.exists():
#                     request.session[address_type + "_address_id"] = shipping_address
#                 if is_safe_url(redirect_path, request.get_host()):
#                     return redirect(redirect_path)
#     return redirect("cart:checkout")