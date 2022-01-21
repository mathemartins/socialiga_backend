from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

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
