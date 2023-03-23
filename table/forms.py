'''from django import forms  
from .models import *
import django.contrib.auth.models 
from django import forms



class SNJ(forms.ModelForm):
    shift = forms.ModelChoiceField(
        queryset=Shift.objects.all(),
        label="Смена"
    ) 
    reason = forms.ModelChoiceField(
        queryset=Reason.objects.all(),
        label="Причина"
    )

    comment = forms.CharField(required=False,  label="Примечание") 
    length_time = forms.IntegerField(required=False,  label="Продолжительность") 
    date_start=forms.DateField(
    widget=forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}),
                required=False,
                label = "Начало"
    ) 
    date_end=forms.DateField(
    widget=forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}),
                required=False,
                label = "Окончание"
    ) 

    class Meta:
        model = ScheduleNotJob  
        fields = ['shift', 'office', 'post', 'human', 'reason', 'comment', 'date_start', 'length_time', 'date_end'] 
        ordering = ('title', 'initials')


#pip install django-crispy-forms
#pip install crispy-bootstrap5  
'''