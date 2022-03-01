import random
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Avg
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render

from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from orders.models import Order


class SalesAjaxView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.user.is_staff:
            qs = Order.objects.all().by_weeks_range(weeks_ago=5, number_of_weeks=5)
            if request.GET.get('type') == 'week':
                days = 7
                start_date = timezone.now().today() - datetime.timedelta(days=days - 1)
                datetime_list = []
                labels = []
                salesItems = []
                for x in range(days):
                    new_time = start_date + datetime.timedelta(days=x)
                    datetime_list.append(
                        new_time
                    )
                    labels.append(
                        new_time.strftime("%a")  # mon
                    )
                    new_qs = qs.filter(updated__day=new_time.day, updated__month=new_time.month)
                    day_total = new_qs.totals_data()['total__sum'] or 0
                    salesItems.append(
                        day_total
                    )
                # print(datetime_list)

                data['labels'] = labels
                data['data'] = salesItems
            if request.GET.get('type') == '4weeks':
                data['labels'] = ["Four Weeks Ago", "Three Weeks Ago", "Two Weeks Ago", "Last Week", "This Week"]
                current = 5
                data['data'] = []
                for _ in range(5):
                    new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1)
                    sales_total = new_qs.totals_data()['total__sum'] or 0
                    data['data'].append(sales_total)
                    current -= 1
        return Response(data)


class SalesView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_class = IsAuthenticated

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_staff:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return super(SalesView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        qs = Order.objects.all().by_weeks_range(weeks_ago=10, number_of_weeks=10)
        start_date = timezone.now().date() - datetime.timedelta(hours=24)
        end_date = timezone.now().date() + datetime.timedelta(hours=12)
        today_data = qs.by_range(start_date=start_date, end_date=end_date).get_sales_breakdown()
        return {
            'today': today_data,
            'this_week': qs.by_weeks_range(
                weeks_ago=1, number_of_weeks=1
            ).get_sales_breakdown(),
            'last_four_weeks': qs.by_weeks_range(
                weeks_ago=5, number_of_weeks=4
            ).get_sales_breakdown(),
        }
