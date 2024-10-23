


from django.urls import path
from .views import TimeSeriesReport
from .testview import TimeSeriesReportTest

urlpatterns = [
    path(
        "monthly-product-sales/",
        TimeSeriesReport.as_view(),
        name="monthly-product-sales",
    ),

    path(
        "monthly-product-sales-test/",
        TimeSeriesReportTest.as_view(),
        name="monthly-product-sales-test",
    ),
]