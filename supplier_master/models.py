from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Supplier_master(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    mobile=models.BigIntegerField() 
    status=models.IntegerField(default=1)
    timestamp=models.TimeField(auto_now_add=True)
     
    def __str__(self):
      return self.name
     

    class  Meta:
        db_table = 'supplier_master'