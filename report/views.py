from django.shortcuts import render
import datetime
from item_master.models import Item_master
# Create your views here.

def report_by_date(request):
    if request.method=='POST':
        f_date=request.POST['f_date']
        s_date=request.POST['s_date']
        sql='''SELECT 1 as id, im.id,im.item_name as item_name, COALESCE(purchase_qty,0) as pur_qty, COALESCE(sale_qty,0) as sale_qty, 
        (COALESCE(purchase_qty,0)-COALESCE(sale_qty,0)) as avail 
        from item_master im 
          LEFT JOIN
          ( SELECT sum(pd.quantity)  as purchase_qty , pd.item_id from purchase_details pd join purchase_master as pm on pm.id=pd.fkey_id
           where invoice_date  BETWEEN '%s' and '%s' GROUP BY item_id
           ) purchase_details on purchase_details.item_id=im.id 
          LEFT JOIN
          ( SELECT sum(sd.quantity) as sale_qty , sd.item_id from sale_details sd join sale_master as sm on sm.id=sd.fkey_id
           where transfer_date BETWEEN '%s' and '%s' GROUP BY item_id 
           ) sale_details on sale_details.item_id=im.id WHERE status =1 
           GROUP by im.id,im.item_name,purchase_qty,sale_qty;'''%(f_date,s_date,f_date,s_date)

        allData=Item_master.objects.raw(sql)
        #print(allData)
        return render(request,'report_by_date.html',{'allData':allData})
    return render(request,'report_by_date.html')

