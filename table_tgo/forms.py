from bootstrap_modal_forms.forms import BSModalModelForm
from .models import TGO, TGO_object, RessourceOperation, Operation
from django import forms

class TGOModelForm(BSModalModelForm):
    class Meta:
        model = TGO
        exclude = ['timestamp']


class UnstyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UnstyledForm, self).__init__(*args, **kwargs)


class TGO_objectModelForm(BSModalModelForm, UnstyledForm):
    class Meta:
        model = TGO_object
        fields = ('tgo', 'operation', 'order')
        widgets = {'tgo': forms.HiddenInput()}
        exclude = ['timestamp']


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


#Для множественного добавления
from django.core.validators import MinValueValidator
class TGOFormset(forms.Form):
    order = forms.IntegerField(validators=[MinValueValidator(1)])
    class Meta:
        model = TGO_object
        fields = ('order', 'operation',)
        exclude = ['timestamp']
