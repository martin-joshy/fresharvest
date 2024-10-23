# from cart.models import OrderItem
# from django.db import models
# from slick_reporting.generator import ReportGenerator



# class SalesReportGenerator(models.Model, ReportGenerator):
#     group_by = 'order__order_date'
#     date_field = 'order__order_date' 

#     queryset = OrderItem.objects.select_related('order', 'product')
         

#     def calculate_total_coupon_discount(self, obj, **kwargs):
#         return obj.order.coupon_discount

#     def calculate_order_discount(self, obj, **kwargs):
#         return obj.discount * obj.qty

#     def calculate_profit(self, obj, **kwargs):
#         total_price = obj.qty * obj.price
#         return total_price - self.calculate_order_discount(obj) - self.calculate_total_coupon_discount(obj)
