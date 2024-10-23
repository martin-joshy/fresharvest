from datetime import timedelta
from django.utils import timezone
from store.models import Product
from cart.models import Order
from datetime import datetime

def generate_sales_report(timeframe, start_date=None, end_date=None):
    if start_date is None:
        if timeframe == 'daily':
            start_date = timezone.now() - timedelta(days=30)
        elif timeframe == 'monthly':
            start_date = timezone.now() - timedelta(days=365)
        elif timeframe == 'yearly':
            start_date = timezone.now() - timedelta(days=365 * 5)

    
    if end_date is None:
        end_date = timezone.now()

   

    report_data = []

    if timeframe == 'daily':
        current_date = start_date
        while current_date <= end_date:
            # Get orders for the current day
            orders = Order.objects.filter(order_date__date=current_date)

            total_sales = 0
            total_discounts = 0
            total_coupon_discounts = 0

            # Calculate total sales, discounts, and coupon discounts for the current day
            for order in orders:
                order_total = order.calculate_total_price()
                total_sales += order_total
                total_discounts += sum(item.discount for item in order.orderitem_set.all())
                total_coupon_discounts += order.coupon_discount

            # Prepare the report data for the current day

            total_discounts = abs(total_discounts)    
            
            report_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'total_sales': total_sales,
                'total_discounts': total_discounts,
                'total_coupon_discounts': total_coupon_discounts,
                'net_sales': total_sales - total_discounts - total_coupon_discounts,
            })

            # Move to the next day
            current_date += timedelta(days=1)
     



    elif timeframe == 'monthly':
        current_month = start_date.replace(day=1)
        while current_month <= end_date.replace(day=1):
            next_month = current_month + timedelta(days=32)
            next_month = next_month.replace(day=1)
            # Get orders for the current month
            orders = Order.objects.filter(order_date__gte=current_month, order_date__lt=next_month)

            total_sales = 0
            total_discounts = 0
            total_coupon_discounts = 0

            # Calculate total sales, discounts, and coupon discounts for the current month
            for order in orders:
                order_total = order.calculate_total_price()
                total_sales += order_total
                total_discounts += sum(item.discount for item in order.orderitem_set.all())
                total_coupon_discounts += order.coupon_discount

            # Prepare the report data for the current month
                
            total_discounts = abs(total_discounts)
            
            report_data.append({
                'date': current_month.strftime('%b-%Y'),
                'total_sales': total_sales,
                'total_discounts': total_discounts,
                'total_coupon_discounts': total_coupon_discounts,
                'net_sales': total_sales - total_discounts - total_coupon_discounts,
            })

            # Move to the next month
            current_month = next_month


    elif timeframe == 'yearly':
        current_year = start_date.year
        while current_year <= end_date.year:
            # Get orders for the current year
            orders = Order.objects.filter(order_date__year=current_year)

            total_sales = 0
            total_discounts = 0
            total_coupon_discounts = 0

            # Calculate total sales, discounts, and coupon discounts for the current year
            for order in orders:
                order_total = order.calculate_total_price()
                total_sales += order_total
                total_discounts += sum(item.discount for item in order.orderitem_set.all())
                total_coupon_discounts += order.coupon_discount

            # Prepare the report data for the current year
            
            total_discounts = abs(total_discounts)

            report_data.append({
                'date': current_year,
                'total_sales': total_sales,
                'total_discounts': total_discounts,
                'total_coupon_discounts': total_coupon_discounts,
                'net_sales': total_sales - total_discounts - total_coupon_discounts,
            })

            # Move to the next year
            current_year += 1


    return report_data, start_date, end_date
