from urllib import request
from django.shortcuts import render,redirect
from django.contrib import messages

from supplier_master.forms import Supplier_master_form
from .models import Supplier_master

# Create your views here.
def supplier_master_list(request):
    allData=Supplier_master.objects.filter(status=1)
    for a in allData:
      print(a)
    return render(request,'supplier_master_list.html',{'allData':allData})

def supplier_master_add_supplier(request):
  if request.method == 'POST':
   forms=Supplier_master_form(request.POST)
   if forms.is_valid():
      if Supplier_master.objects.filter(status=1,name=request.POST['name']):
        messages.success(request,'Supplier Already Exists')
        return redirect('/supplier_master/supplier_master_list/') 
      else:
        forms.save() 
        messages.success(request,'Supplier Added')
        return redirect('/supplier_master/supplier_master_list') 
  else:      
     forms=Supplier_master_form()
     return render(request,'supplier_master_add_supplier.html',{'forms':forms})

def supplier_master_supplier_delete(request,sid):
         selectedData=Supplier_master.objects.get(id=sid) 
         print(selectedData)  
         selectedData.status=0
         selectedData.save() 
         messages.success(request,"Item Deleted")   
         return redirect('/supplier_master/supplier_master_list')     