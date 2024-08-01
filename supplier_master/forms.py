from django import forms

from supplier_master.models import Supplier_master

class Supplier_master_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Supplier_master_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['name'].required =True
        self.fields['mobile'].required = True
        self.fields['address'].required = True
        
    
    class Meta:
        model = Supplier_master
        fields = ('name','mobile','address')
        widgets={
             'name':forms.TextInput(attrs={'class':'form-control', 'id':'name','name':'name',}),
             'mobile':forms.TextInput(attrs={'class':'form-control', 'id':'mobile','name':'mobile','maxlength':'10'}),
             'address':forms.TextInput(attrs={'class':'form-control', 'id':'address','name':'address'}),
        }
        

