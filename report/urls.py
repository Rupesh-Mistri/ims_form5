
from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_by_date),
    

 
]
