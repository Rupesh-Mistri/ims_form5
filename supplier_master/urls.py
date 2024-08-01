from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_master_list),
    path('supplier_master_list/', views.supplier_master_list),
    path('supplier_master_add_supplier/', views.supplier_master_add_supplier),
    path('supplier_master_supplier_delete/<sid>',views.supplier_master_supplier_delete)
]