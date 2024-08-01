from unicodedata import decimal
from django.db import models

# Create your models here.
class Item_master(models.Model):
    status=models.IntegerField(default=1)
    stampdatetime=models.DateField(auto_now=True)
    item_name = models.CharField(max_length=50)
    rate      = models.CharField(max_length=50)
    def __str__(self):
        return self.item_name
    class  Meta:
        db_table = 'item_master'
    

  