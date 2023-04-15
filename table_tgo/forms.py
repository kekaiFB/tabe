'''from bootstrap_modal_forms.forms import BSModalModelForm
from .models import TGO, TGO_object, RessourceOperation
from django import forms

class TGOModelForm(BSModalModelForm):
    class Meta:
        model = TGO
        fields = ('title',)
        exclude = ['timestamp', 'user']


class UnstyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UnstyledForm, self).__init__(*args, **kwargs)
        

class TGO_objectModelForm(BSModalModelForm, UnstyledForm):
    class Meta:
        model = TGO_object
        fields = ('tgo', 'operation', 'order')
        widgets = {'tgo': forms.HiddenInput()}
        exclude = ['timestamp',  'user']


class RessourceOperationModelForm(BSModalModelForm, UnstyledForm):
    class Meta:
        model = RessourceOperation
        fields = '__all__'
        widgets = {'tgo': forms.HiddenInput(),
                   'tgo_object': forms.HiddenInput(),
                   'time_start': forms.HiddenInput(),
                   'time_lenght': forms.HiddenInput(),
                   'time_end': forms.HiddenInput(),
                   }
        exclude = ['timestamp']
'''