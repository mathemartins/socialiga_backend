from rest_framework import status
from rest_framework.response import Response


class IsVendor(object):
    def initial(self, request, *args, **kwargs):
        if request.user.profile.account_type != 'VENDOR':
            return Response({'message': status.HTTP_403_FORBIDDEN})