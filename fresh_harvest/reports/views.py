from django.shortcuts import render
from .report import generate_sales_report
from datetime import datetime


def sales_report_view(request):

    if request.method == 'POST':

        timeframe = request.POST.get('timeframe')
        
        end_date = request.POST.get('end_date')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date = None

        start_date = request.POST.get('start_date')
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_date = None
        


        report_data, start_date, end_date = generate_sales_report(timeframe, start_date, end_date)


        heading = f"{timeframe} Report from {start_date.date()} to {end_date.date()}"

        return render(request, 'report.html', {'report_data': report_data, 'heading': heading})

    return render(request, 'report.html')