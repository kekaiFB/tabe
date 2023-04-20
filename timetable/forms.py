from bootstrap_modal_forms.forms import BSModalModelForm
from .models import (Airlines
                     , Airplane
                     , EquipmentAirplane
                     , TypeCountry
                     , Country
                     , City
                     , Airport
                     , TypeFlight
                     , Flight
                     , TtimetableStatus
                     , Ttimetable
                     )
from django import forms


class TimeTableModelForm(BSModalModelForm):
    class Meta:
        model = Ttimetable
        fields = '__all__'

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
        model = TtimetableStatus
        fields = '__all__'

class FlightModelForm(BSModalModelForm):
    class Meta:
        model = Flight
        fields = '__all__'



