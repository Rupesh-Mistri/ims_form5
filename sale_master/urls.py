
from django.urls import path
from . import views

urlpatterns = [
    path('', views.sale_master_list),
    path('sale_master_list/', views.sale_master_list),
    path('sale_master_add_sale/', views.sale_master_add_sale),
    path('get_value_for_textbox_sale',views.get_value_for_textbox_sale),
    path('get_value_for_stock_left_sale',views.get_value_for_stock_left_sale),
    path('sale_master_view/<smid>',views.sale_master_view)
   
 
]
