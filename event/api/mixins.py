from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from rest_framework.reverse import reverse


class StaffMemberRequiredAPIMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffMemberRequiredAPIMixin, self).dispatch(request, *args, **kwargs)


class AccountTypeCUSTOMERORVENDORAPIMixin(object):
    def dispatch(self, request, *args, **kwargs):
        print(self.request.user.profile.account_type)
        if self.request.user.profile.account_type == 'CUSTOMER':
            return HttpResponseRedirect(reverse('404'))
        return super(AccountTypeCUSTOMERORVENDORAPIMixin, self).dispatch(request, *args, **kwargs)
