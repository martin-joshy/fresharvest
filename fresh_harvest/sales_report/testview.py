# from django.utils.translation import gettext_lazy as _
# from django.db.models import Sum
# from slick_reporting.views import ReportView, Chart
# from slick_reporting.fields import ComputationField
# from .models import Sales
# from .reports import SalesReportGenerator 
# from slick_reporting.generator import ReportGenerator
# from cart.models import Order



# class TimeSeriesReportTest(ReportView):
#     report_model = Order
#     # group_by = "product"

#     time_series_pattern = "monthly"
#     # options are: "daily", "weekly", "bi-weekly", "monthly", "quarterly", "semiannually", "annually" and "custom"

#     date_field = "order_date"

#     # These columns will be calculated for each period in the time series.
#     time_series_columns = [
#         ComputationField.create(Sum, "calculate_total_price", verbose_name=_("Sales For Month")),
#     ]

#     columns = [
#         "user", 
#         "__time_series__",
#         # This is the same as the time_series_columns, but this one will be on the whole set
#         ComputationField.create(Sum, "calculate_total_price", verbose_name=_("Total Sales")),
#     ]

#     chart_settings = [
#         Chart(
#             "Client Sales",
#             Chart.BAR,
#             data_source=["sum__calculate_total_price"],
#             title_source=["user"],
#         ),
#         Chart(
#             "Total Sales Monthly",
#             Chart.PIE,
#             data_source=["sum__calculate_total_price"],
#             title_source=["user"],
#             plot_total=True,
#         ),
#         Chart(
#             "Total Sales [Area chart]",
#             Chart.AREA,
#             data_source=["sum__calculate_total_price"],
#             title_source=["user"],
#         ),
#     ]