from django.db import models

class Sale_master(models.Model):
    transfer_no=models.IntegerField()
    transfer_date=models.DateField()
    customer_id=models.CharField(max_length=100)    
    status=models.IntegerField(default=1)
    sale_date=models.DateField(auto_now=True)
    customer_address=models.CharField(max_length=100)

    class  Meta:
        db_table = 'sale_master'



class Temp_sale_details(models.Model):
    status=models.IntegerField(default=1)
    stampdatetime=models.DateField(auto_now=True)
    item_id =models.IntegerField()
    rate=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.IntegerField()
    total=models.DecimalField(max_digits=10,decimal_places=2)
    
    class  Meta:
        db_table = 'temp_sale_details'    

class Sale_details(models.Model):
    status=models.IntegerField(default=1)
    stampdatetime=models.DateField(auto_now=True)
    item_id =models.IntegerField()
    rate=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.IntegerField()
    total=models.DecimalField(max_digits=10,decimal_places=2)
    fkey =models.ForeignKey(Sale_master,  on_delete=models.CASCADE)

    class  Meta:
        db_table = 'sale_details'    

