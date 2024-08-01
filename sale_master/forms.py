from cProfile import label
from unittest.util import _MAX_LENGTH
from django import forms

from purchase_master.models import Purchase_details
from .models import Sale_master,Sale_details
from item_master.models import Item_master

class Sale_master_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Sale_master_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['transfer_no'].required =True
        self.fields['transfer_date'].required = True
        self.fields['customer_id'].required = True
        self.fields['customer_address'].required = True
        
    class Meta:
        model =Sale_master
        fields = ('transfer_no','transfer_date','customer_id','customer_address')

        labels={
            'transfer_no':'Transfer No',
            'transfer_date':'Transfer Date',
            'customer_id':'Customer Name',
            'customer_address':'Customer Address',
        }
        widgets={
            'transfer_no':forms.TextInput(attrs={'class':'form-control', 'id':'transfer_no','name':'transfer_no','type':'number'}),
            'transfer_date':forms.DateInput(attrs={'class':'form-control', 'id':'transfer_date','name':'transfer_date','format':"%m/%d/%Y",'type':'date' }),
            'customer_id':forms.TextInput(attrs={'class':'form-control', 'id':'customer_id','name':'customer_id',}),
            'customer_address':forms.TextInput(attrs={'class':'form-control', 'id':'customer_address','name':'customer_address',}),

        }     


class Sale_details_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Sale_details_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['item_id'].required =True
        self.fields['rate'].required = True
        self.fields['quantity'].required = True
        self.fields['total'].required = True
    item_id=forms.ModelChoiceField(queryset=Item_master.objects.filter(id__in=Purchase_details.objects.values('item_id').distinct()),empty_label='Select', widget=forms.Select(attrs={"class":'form-control'}))
    #avail_qu=forms.TextInput()
    class Meta:
        model = Sale_details
        fields = ('item_id','rate','quantity','total')
        widgets={
            'item_id':forms.TextInput(attrs={'class':'form-control','id':'item_id','name':'item_id'}),
            'rate':forms.TextInput(attrs={'class':'form-control','id':'rate','name':'rate'}),
            'quantity':forms.TextInput(attrs={'class':'form-control','id':'quantity','name':'quantity'}),
            'total':forms.TextInput(attrs={'class':'form-control','id':'total','name':'total'}),
            'avail_qu':forms.TextInput(attrs={'class':'form-control','id':'avail_qu','name':'avail_qu'}),
        }    

class Sale_stock_avail(forms.Form):
    avail_qu=forms.Textarea()
    