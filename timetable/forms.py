from bootstrap_modal_forms.forms import BSModalModelForm
from .models import *
from django import forms


class UnstyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(UnstyledForm, self).__init__(*args, **kwargs)
        

class TimeTableModelForm(BSModalModelForm,UnstyledForm): 
    arrival_time = forms.CharField(
        widget=forms.TimeInput(
            attrs={'type': 'time'},
            format='%H:%M'
        ), 
        label = "Прилет"
    )
    departure_time = forms.CharField(
        widget=forms.TimeInput(
            attrs={'type': 'time'},
            format='%H:%M'
        ), 
        label = "Вылет"
    )
    date_start=forms.DateField(
        widget=forms.DateInput(
                    format=('%Y-%m-%d'),
                    attrs={'type': 'date'}),
        required=False,
        label = "Начало действия"
    )  
    date_end=forms.DateField(
        widget=forms.DateInput(
                    format=('%Y-%m-%d'),
                    attrs={'type': 'date'}),
        required=False,
        label = "Конец действия"
    )  

    start_register_time = forms.CharField(
        widget=forms.TimeInput(
            attrs={'type': 'time'},
            format='%H:%M'
        ),
        label = "Начало Регистрации"
    )
    
    end_register_time = forms.CharField(
        widget=forms.TimeInput(
            attrs={'type': 'time'},
            format='%H:%M'
        ), 
        label = "Конец Регистрации"
    )
        
    class Meta:
        model = Timetable
        widgets = {'timetablelist': forms.HiddenInput()}
        exclude = [ 'author', 'editor']

class AirlinesModelForm(BSModalModelForm):
    class Meta:
        model = Airlines
        fields = '__all__'

class AirplaneModelForm(BSModalModelForm):
    class Meta:
        model = Airplane
        fields = '__all__'

class EquipmentAirplaneModelForm(BSModalModelForm):
    class Meta:
        model = EquipmentAirplane
        fields = '__all__'

class TypeCountryModelForm(BSModalModelForm):
    class Meta:
        model = TypeCountry
        fields = '__all__'

class CountryModelForm(BSModalModelForm):
    class Meta:
        model = Country
        fields = '__all__'

class CityModelForm(BSModalModelForm):
    class Meta:
        model = City
        fields = '__all__'

class AirportModelForm(BSModalModelForm):
    class Meta:
        model = Airport
        fields = '__all__'

class TypeFlightModelForm(BSModalModelForm):
    class Meta:
        model = TypeFlight
        fields = '__all__'

class TimetableStatusModelForm(BSModalModelForm):
    class Meta:
        model = TimetableStatus
        fields = '__all__'


class FlightModelForm(BSModalModelForm):
    class Meta:
        model = Flight
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        airport = [(Airport.id, Airport.__str__()) for Airport in Airport.objects.all()]
        self.fields['departurelAirport'].choices = airport
        self.fields['arrivalAirport'].choices = airport

        city = [(City.id, City.__str__()) for City in City.objects.all()]
        self.fields['departure'].choices = city
        self.fields['arrival'].choices = city



class HistoryTimetableModelForm(BSModalModelForm):
    class Meta:
        model = Timetable
        fields = '__all__'

class TimetableListModelForm(BSModalModelForm):
    class Meta:
        model = TimetableList
        fields = ('title',)
        exclude = ['user']