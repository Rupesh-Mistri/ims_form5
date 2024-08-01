from django.shortcuts import render,redirect
from purchase_master.models import Purchase_details
import sale_master
from sale_master.models import Sale_master,Temp_sale_details,Sale_details
from .forms import Sale_details_form, Sale_master_form,Sale_stock_avail
from django.contrib import messages

# Create your views here.
def sale_master_list(request):
    sql='''SELECT sale_master.id,sale_master.id as click,transfer_no, transfer_date, CONCAT(sale_master.id ,'-',transfer_date) AS sale_id,customer_id FROM sale_master JOIN sale_details on sale_master.id=sale_details.Fkey_id group by sale_master.id;'''
    allData=Purchase_details.objects.raw(sql)
    print(allData)
    return render(request,'sale_master_list.html',{'allData':allData})

def sale_master_add_sale(request):
    # allData=Temp_sale_details.objects.raw('''select item_master.id,item_name,temp_sale_details.rate,quantity,quantity*temp_sale_details.rate as total 
    #                                              from temp_sale_details  left join item_master on  temp_sale_details.item_id=item_master.id''')
    allData=Temp_sale_details.objects.raw('''select item_master.id,item_name,temp_sale_details.rate,quantity,quantity*temp_sale_details.rate as total 
    
                                                 from item_master  join temp_sale_details on  item_master.id=temp_sale_details.item_id''')
    forms_sm=Sale_master_form(request.POST)
    forms_sd=Sale_details_form(request.POST)
    forms_sa=Sale_stock_avail(request.POST)
    
    if request.method=='POST':
      #print("clicked")
      if 'addbtn' in request.POST:
        
        forms_sm=Sale_master_form(request.POST)
        print("sale add  clicked")
          
        item_id=request.POST.get("item_id")
        rate=request.POST.get("rate")
        quantity=request.POST.get("quantity")
        total=request.POST.get("total")
        avail_qu=request.POST.get('avail_qu')
        
        if (int(quantity)<=int(avail_qu) and int(quantity)>0):
          Temp_sale_details.objects.create(
            item_id=item_id,
            rate=rate,
            quantity=quantity,
            total=total,
            
           )
          return redirect('/sale_master/sale_master_add_sale/')
        else:
            messages.success(request,'You have entered Wrong Quantity')
            return render(request,'sale_master_add_sale.html',{'forms_sm':forms_sm,'forms_sd':forms_sd,'forms_sa':forms_sa,'allData':allData})
         
      if 'savebtn' in request.POST:  
        
          transfer_no=request.POST.get("transfer_no")
          transfer_date=request.POST.get("transfer_date")
          customer_id=request.POST.get("customer_id")
          customer_address=request.POST.get("customer_address")
          if Sale_master.objects.filter(status=1,transfer_no=transfer_no):
            messages.success(request,'This Transfer No. already Exist')
            return redirect('sale_master/sale_master_add_sale')
          else:  
            Sale_master.objects.create(
               transfer_no=transfer_no,
               transfer_date=transfer_date,
               customer_id=customer_id,
               customer_address=customer_address,
             )

            a=Temp_sale_details.objects.all()
            for data in a:
              print(data)
              Sale_details.objects.create(
                  item_id=data.item_id,
                  rate=data.rate,
                  quantity=data.quantity,
                  total=data.total,
                  fkey_id=Sale_master.objects.latest('id').id
                 )

            d=Temp_sale_details.objects.all().delete()
            return redirect('/sale_master/sale_master_list/')
    
    else:    
      allData=Temp_sale_details.objects.raw('''select item_master.id,item_name,temp_sale_details.rate,quantity,quantity*temp_sale_details.rate as total 
    
                                                 from item_master  join temp_sale_details on  item_master.id=temp_sale_details.item_id''') 
      forms_sm=Sale_master_form()
      forms_sd=Sale_details_form()
      return render(request,'sale_master_add_sale.html',{'forms_sm':forms_sm,'forms_sd':forms_sd,'allData':allData})

def get_value_for_textbox_sale(request):
    un=request.GET['un']
    print("Ajax")
    t=Purchase_details.objects.raw('''select id,rate from purchase_details where item_id='%s' order by id DESC limit 1'''%(un))
    return render(request,'rate.html',{'t':t}) 

def get_value_for_stock_left_sale(request):
    un=request.GET['un']
    #t=Item_master.objects.raw('select i.id,COALESCE(sum(pur_qty-sale_qty), pur_qty)as stock_left from item_master i left join ( select item_id,sum(p.quantity) as pur_qty from purchase_details p group by item_id ) as pur on i.id=pur.item_id left join ( select item_id, COALESCE(sum(s.quantity), 0) as sale_qty from sale_details s group by item_id ) as sal on i.id=sal.item_id where i.id='+un+' group by i.id;')
    t=Purchase_details.objects.raw('''
          select i.id, (COALESCE(pur_qty,0)-COALESCE(sale_qty,0)-COALESCE(tsale_qty,0)) as stock_left from item_master i 
      left join 
      ( select item_id,sum(p.quantity) as pur_qty from purchase_details p group by item_id 
       ) as pur on i.id=pur.item_id 
       left join 
       ( select item_id, COALESCE(sum(s.quantity), 0) as sale_qty from sale_details s group by item_id
       ) as sal on i.id=sal.item_id 
       left join
       ( select item_id, COALESCE(sum(ts.quantity), 0) as tsale_qty from temp_sale_details ts group by item_id
       ) as temp on i.id=temp.item_id 
       where i.id='%s' '''%(un))    #j=json.dumps(t.stock_left)
       
    return render(request,'stock_left.html',{'t':t}) 



def sale_master_view(request,smid):
    sql='''SELECT sale_master.id,transfer_no, transfer_date, CONCAT(sale_master.id ,'-',transfer_date) AS sale_id,customer_id,customer_address as address  FROM sale_master JOIN sale_details on sale_master.id=sale_details.Fkey_id   where sale_master.id='%s' group by sale_master.id ;'''%(smid) 
    allData=Purchase_details.objects.raw(sql)

    sql1='select sm.id ,item_name,sd.rate as rate,quantity ,sd.rate*quantity as total from sale_details sd JOIN sale_master sm ON sm.id=sd.fkey_id JOIN item_master i ON i.id=sd.item_id where sm.id='+smid+'  group by sd.rate,sd.quantity , sm.id , item_name'
     
    allData1=Purchase_details.objects.raw(sql1)

    print(allData)
    return render(request,'sale_master_view.html',{'allData':allData,'allData1':allData1})
