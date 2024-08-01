
from django import forms
from item_master.models import Item_master

from supplier_master.models import Supplier_master
from .models import Purchase_details, Purchase_master


class Purchase_master_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Purchase_master_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['invoice_no'].required =True
        self.fields['invoice_date'].required = True
        self.fields['supplier_id'].required = True

    supplier_id=forms.ModelChoiceField(queryset=Supplier_master.objects.filter(status=1),empty_label='Select',label='Supplier', widget=forms.Select(attrs={"class":'form-control'}))
    class Meta:
        model = Purchase_master
        fields = ('invoice_no','invoice_date','supplier_id')
         
        labels={
            'invoice_no':'Invoice No',
            'invoice_date':'Invoice Date',
            
        }
        widgets={
            'invoice_no':forms.TextInput(attrs={'class':'form-control', 'id':'invoice_no','name':'invoice_no','type':'number'}),
            'invoice_date':forms.DateInput(attrs={'class':'form-control', 'id':'invoice_date','name':'invoice_date','format':"%m/%d/%Y",'type':'date' }),
  
        }


class Purchase_details_form(forms.ModelForm): 
    item_id=forms.ModelChoiceField(queryset=Item_master.objects.filter(status=1),empty_label='Select', widget=forms.Select(attrs={"class":'form-control'}))
    def __init__(self, *args, **kwargs):
        super(Purchase_details_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['item_id'].required =True
        self.fields['rate'].required = True
        self.fields['quantity'].required = True
        self.fields['total'].required = True
    class Meta:
        model = Purchase_details
        fields = ('item_id','rate','quantity','total')
        widgets={
            'item_id':forms.TextInput(attrs={'class':'form-control','id':'item_id','name':'item_id'}),
            'rate':forms.TextInput(attrs={'class':'form-control','id':'rate','name':'rate'}),
            'quantity':forms.TextInput(attrs={'class':'form-control','id':'quantity','name':'quantity'}),
            'total':forms.TextInput(attrs={'class':'form-control','id':'total','name':'total'}),
        }
        
        

