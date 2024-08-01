
from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchase_master_list),
    path('purchase_master_list/', views.purchase_master_list),
    path('purchase_master_add_purchase/', views.purchase_master_add_purchase),
    path('get_value_for_textbox/', views.get_value_for_textbox),
    path('get_value_for_span/', views.get_value_for_span),
    path('purchase_master_view/<pid>',views.purchase_master_view),
   
 
]
