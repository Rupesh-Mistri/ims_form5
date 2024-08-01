from email import message
from urllib import request
from django.shortcuts import render,redirect
import purchase_master
from purchase_master.forms import Purchase_details_form, Purchase_master_form
from .models import Purchase_master,Temp_purchase_details,Purchase_details
from item_master.models import Item_master
from django.http import JsonResponse,HttpResponse
from django.contrib import messages


# Create your views here.
def purchase_master_list(request):
    sql='''SELECT purchase_master.id,purchase_master.id as click ,invoice_no, invoice_date, 
    CONCAT(purchase_master.id ,'-',invoice_date) AS purchase_id,supplier_master.name as supplier 
    FROM purchase_master 
    JOIN purchase_details on purchase_master.id=purchase_details.Fkey_id 
    join supplier_master on supplier_master.id=purchase_master.supplier_id_id group by purchase_master.id,supplier_master.name;
         '''
    allData=Purchase_master.objects.raw(sql)
    print(allData)
    return render(request,'purchase_master_list.html',{'allData':allData})
    
def purchase_master_add_purchase(request):
    allData=Temp_purchase_details.objects.raw('''select item_master.id,item_name,temp_purchase_details.rate,quantity,quantity*temp_purchase_details.rate as total 
                                                 from temp_purchase_details join item_master on  temp_purchase_details.item_id=item_master.id''')
    
    forms_pm=Purchase_master_form(request.POST)
    forms_pd=Purchase_details_form(request.POST)
       
    # invoice_no=request.POST.get('invoice_no')
    # invoice_date=request.POST.get('invoice_date')
    # Supplier_id=request.POST.get('Supplier_id')
   
    if request.method=='POST':
      #print("clicked")
      if 'addbtn' in request.POST:
        # forms_pm=Purchase_master_form(request.POST)
        forms_pd=Purchase_details_form(request.POST)
        print("purchAE add  clicked")
        # if forms_pd.is_valid():
        #      forms_pd.save()  
        item_id=request.POST.get("item_id")
        rate=request.POST.get("rate")
        quantity=request.POST.get("quantity")
        total=request.POST.get("total")
        
        Temp_purchase_details.objects.create(
            item_id=item_id,
            rate=rate,
            quantity=quantity,
            total=total,
            
        )
        # forms_pd=Purchase_details_form()
        # return render(request,'purchase_master_add_purchase.html',{'forms_pm':forms_pm,'forms_pd':forms_pd,'allData':allData})
        return redirect('/purchase_master/purchase_master_add_purchase/')
        
      if 'savebtn' in request.POST:  
          invoice_no=request.POST["invoice_no"]
          invoice_date=request.POST["invoice_date"]
          supplier_id=request.POST["supplier_id"]
          if Purchase_master.objects.filter(status=1,invoice_no=invoice_no):
             messages.success(request,' This Invoice No. already exist')
             return redirect('/purchase_master/purchase_master_add_purchase/')
          else:   
            Purchase_master.objects.create(
               invoice_no=invoice_no,
               invoice_date=invoice_date,
               supplier_id_id=supplier_id,
             )

            a=Temp_purchase_details.objects.all()
            for data in a:
              print(data)
              Purchase_details.objects.create(
                  item_id=data.item_id,
                  rate=data.rate,
                  quantity=data.quantity,
                  total=data.total,
                  fkey_id=Purchase_master.objects.latest('id').id
                 )

            d=Temp_purchase_details.objects.all().delete()
            return redirect('/purchase_master/purchase_master_list/')
    #   if forms_pm.is_valid():
        # forms_pm.save()
    #   if forms_pd.is_valid():
        # forms_pd.save()  
    else: 
      allData=Temp_purchase_details.objects.raw('''select item_master.id,item_name,temp_purchase_details.rate,quantity,quantity*temp_purchase_details.rate as total 
                                                 from temp_purchase_details join item_master on  temp_purchase_details.item_id=item_master.id''')
     
      forms_pm=Purchase_master_form()
      forms_pd=Purchase_details_form()
      return render(request,'purchase_master_add_purchase.html',{'forms_pm':forms_pm,'forms_pd':forms_pd,'allData':allData})
            
def get_value_for_span(request):
    un=request.GET['un']
    print("Ajax")
    #print("ajax "+un+"")
    t=Item_master.objects.raw('''select id,address from supplier_master where id='%s' '''%(un))
    
    #res={'status':'success','rate':t.rate}
   
    return render(request,'address.html',{'t':t}) 


def get_value_for_textbox(request):
    un=request.GET['un']
    print("Ajax")
    #print("ajax "+un+"")
    t=Item_master.objects.raw('''select id,rate from item_master where id='%s' '''%(un))
    
    #res={'status':'success','rate':t.rate}
   
    return render(request,'rate.html',{'t':t}) 
    #return HttpResponse({ 't':t.rate}) 
    #return   JsonResponse({'t':t})         

def purchase_master_view(request,pid):
    sql='''SELECT purchase_master.id,invoice_no, invoice_date, CONCAT(purchase_master.id ,'-',invoice_date) AS purchase_id,supplier_master.name as supplier, supplier_master.address as address FROM purchase_master JOIN purchase_details on purchase_master.id=purchase_details.Fkey_id join supplier_master on supplier_master.id=purchase_master.supplier_id_id  where purchase_master.id='%s' group by supplier_master.address,supplier_master.name, purchase_master.id ;'''%(pid)
           
    allData=Purchase_details.objects.raw(sql)

    sql1='''select pm.id ,item_name,pd.rate as rate,quantity ,pd.rate*quantity as total from purchase_details pd JOIN purchase_master pm ON pm.id=pd.fkey_id JOIN item_master i ON i.id=pd.item_id where pm.id='%s' group by pd.quantity, pm.id,pd.rate,item_name'''%(pid)

    allData1=Purchase_details.objects.raw(sql1)

   # sql = """select i.id,sum(p.quantity) as pqty, i.item_name as itemn from purchase_details p join item_master i on p.item_id=i.id join sale_details s on s.item_id=i.id group by item_id, item_name """
   # sql="select id,item_name,rate from item_master"
  
    print(allData)
    return render(request,'purchase_master_view.html',{'allData':allData,'allData1':allData1})
    