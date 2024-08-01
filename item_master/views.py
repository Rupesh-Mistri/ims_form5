from django.shortcuts import render,redirect
from django.http import HttpResponse
from item_master.models import Item_master
from .forms import Item_master_form
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger\

# Create your views here.
# def item_master_list(request):
#    allData=Item_master.objects.raw('select * from item_master where status=1 group by id,item_name') #final
#    for a in allData:
#       print(a)
#    return render(request,'item_master_list.html',{"allData":allData})

def item_master_list(request):
   allData=Item_master.objects.raw('select * from item_master where status=1 group by id,item_name') #final
   for a in allData:
      print(a)
   paginator = Paginator(allData, 2)
    
   page = request.GET.get('page')
   try:
      page_object = paginator.page(page)
   except PageNotAnInteger:
      page_object = paginator.page(1)
   except EmptyPage:
      page_object = paginator.page(paginator.num_pages)

   allData = page_object
   return render(request,'item_master_list.html',{"allData":allData,'page_obj':allData})

def item_master_add_item(request) :
   if request.method == 'POST':
    forms=Item_master_form(request.POST)
    if forms.is_valid():
       
       if Item_master.objects.filter(status=1,item_name=request.POST['item_name']):
        messages.success(request,'Item Already Exist')
        return redirect('/item_master/item_master_list')   
       else:
          forms.save() 
          messages.success(request,'Item Added')
          return redirect('/item_master/item_master_list') 
   else:     
    forms=Item_master_form() 
    return render(request,'item_master_add_item.html',{'forms':forms})    

def item_master_item_view(request,item_id) :
        selectedData=Item_master.objects.get(id=item_id)
        print(selectedData)
        forms=Item_master_form(instance=selectedData)  
        return render(request,'item_master_item_view.html',{'selectedData':selectedData,'forms':forms})

def item_master_item_update(request,item_id):
        if request.method == 'POST':
         forms=Item_master_form(request.POST)
         if forms.is_valid():
          update=Item_master.objects.filter(id=item_id).update(
                    item_name=request.POST["item_name"],
                    rate=request.POST["rate"]
                    )
          messages.success(request, 'Updated Successfully')           
          return redirect('/item_master/item_master_list')   
        else:
         selectedData=Item_master.objects.get(id=item_id)
         forms=Item_master_form(instance=selectedData)
         print(selectedData)
         return render(request,'item_master_item_update.html',{'selectedData':selectedData,'forms':forms})

def item_master_item_delete(request,item_id):
         selectedData=Item_master.objects.get(id=item_id) 
         print(selectedData)  
         selectedData.status=0
         selectedData.save()
         messages.success(request,"Item Deleted")   
         return redirect('/item_master/item_master_list')
