
# from django.utils.translation import gettext_lazy as _
# from django.db.models import Sum
# from slick_reporting.views import ReportView, Chart
# from slick_reporting.fields import ComputationField
# from .models import Sales
# from .reports import SalesReportGenerator 
# from slick_reporting.generator import ReportGenerator



# class TimeSeriesReport(ReportView):
#     report_model = SalesReportGenerator
#     # group_by = "product"

#     time_series_selector = True

#     time_series_selector_choices = (
#         ("daily", _("Daily")),
#         ("weekly", _("Weekly")),
#         ("bi-weekly", _("Bi-Weekly")),
#         ("monthly", _("Monthly")),
#     )
#     time_series_selector_default = "bi-weekly"

#     time_series_selector_label = _("Period Pattern")
#     # The label for the time series selector

#     time_series_selector_allow_empty = True

#     date_field = "order__order_date"

#     # These columns will be calculated for each period in the time series.
#     time_series_columns = [
#         ComputationField.create(Sum, 'calculate_total_coupon_discount', verbose_name=_("Total Coupon Discount")),
#         ComputationField.create(Sum, 'calculate_order_discount', verbose_name=_("Total Order Discount")),
#         ComputationField.create(Sum, 'calculate_profit', verbose_name=_("Total Profit")),
#     ]

    

#     columns = [
#         "product__title",
#         "__time_series__",
#         # This is the same as the time_series_columns, but this one will be on the whole set
#         ComputationField.create(Sum, 'calculate_total_coupon_discount', verbose_name=_("Total Coupon Discount")),
#         ComputationField.create(Sum, 'calculate_order_discount', verbose_name=_("Total Order Discount")),
#         ComputationField.create(Sum, 'calculate_profit', verbose_name=_("Total Profit")),
#     ]


#     chart_settings = [
#         Chart(
#             "Product Sales",
#             Chart.BAR,
#             data_source=["calculate_profit"],
#             title_source=["product__title"],
#         ),
#         Chart(
#             "Total Sales Monthly",
#             Chart.PIE,
#             data_source=["calculate_profit"],
#             title_source=["product__title"],
#             plot_total=True,
#         ),
#         Chart(
#             "Total Sales [Area chart]",
#             Chart.AREA,
#             data_source=["calculate_profit"],
#             title_source=["product__title"],
#         ),
#     ]
