from . import views
from django.urls import path, include

urlpatterns = [

    path( '', views.sales_report_view, name= 'report'),
    
    
]