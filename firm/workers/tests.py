from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from .models import DriverLog
from .views import DriverLogViewSet, DriverLogWeeklyViewSet
from rest_framework.response import Response
from datetime import datetime


class DriverLogViewSetTestCase(TestCase):
    def setUp(self):
        self.log1 = DriverLog.objects.create(driver_id=1, company_id=1, status='working', create_date=timezone.now())
        self.log2 = DriverLog.objects.create(driver_id=1, company_id=1, status='resting', create_date=timezone.now())

    def test_driver_log_view(self):
        factory = APIRequestFactory()
        request = factory.get('/driver-logs/')
        view = DriverLogViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)


class DriverLogWeeklyViewSetTestCase(TestCase):
    def setUp(self):
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())

        self.log1 = DriverLog.objects.create(driver_id=1, company_id=1, status='working',
                                             create_date=week_start + timedelta(days=1))
        self.log2 = DriverLog.objects.create(driver_id=1, company_id=1, status='resting',
                                             create_date=week_start + timedelta(days=2))

    def test_driver_log_weekly_view(self):
        factory = APIRequestFactory()
        request = factory.get('/driver-logs-weekly/')
        view = DriverLogWeeklyViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        print(response.data)  # Print the response data for debugging

        self.assertEqual(len(response.data), 1)
