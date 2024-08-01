
import numbers
from django import forms

from item_master.models import Item_master

class Item_master_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Item_master_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['item_name'].required =True
        self.fields['rate'].required = True

    class Meta:
        model = Item_master
        fields = ("item_name","rate")
        widgets={
          'item_name':forms.TextInput(attrs={'class':'form-control', 'id':'item_name','name':'item_name'}),
          'rate':forms.TextInput(attrs={'class':'form-control','id':'rate','name':'rate','type':'number'})
        }
        labels={
             'item_name':'Item Name',
             'rate':'Rate'
        }
        error_message={
            'item_name': {
                'required': 'Please Enter Item Name',
            },
            'rate': {
                'required': 'Please Enter Rate',
            },
        }


