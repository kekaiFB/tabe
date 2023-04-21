
from django.views.generic import ListView
from .models import (Airlines
                     , Airplane
                     , EquipmentAirplane
                     , TypeCountry
                     , Country
                     , City
                     , Airport
                     , TypeFlight
                     , Flight
                     , Timetable
                     , TimetableStatus
                     )
from django.db.models import Prefetch
from .utils import *
from .forms import *

from bootstrap_modal_forms.generic import (
   BSModalCreateView
  , BSModalDeleteView
  , BSModalUpdateView
)

from django.shortcuts import redirect 

# ---------------------------------Расписание----------------------
class TimeTableView(DataMixin, ListView):
    template_name = 'timetable/index.html'
    context_object_name = 'timetable'
    model = Timetable

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Расписание")
        context = dict(list(context.items()) + list(c_def.items()))
        return context   

class TimeTableCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = TimeTableModelForm
    success_url = reverse_lazy('timetable:index')

class TimeTableUpdateView(BSModalUpdateView):
    model = Timetable
    template_name = 'table_tgo/edit_data/update.html'
    form_class = TimeTableModelForm
    success_url = reverse_lazy('timetable:index')

class TimeTableDeleteView(BSModalDeleteView):
    model = Timetable
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:index')
# -------------------------------------------------------------------


# ---------------------------------Авиакомпании----------------------
class AirlinesView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/airlines_list.html'
    context_object_name = 'airlines'
    model = Airlines

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авиакомпании")
        return dict(list(context.items()) + list(c_def.items()))
    
class AirlinesCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = AirlinesModelForm
    success_url = reverse_lazy('timetable:airlines')

class AirlinesUpdateView(BSModalUpdateView):
    model = Airlines
    template_name = 'table_tgo/edit_data/update.html'
    form_class = AirlinesModelForm
    success_url = reverse_lazy('timetable:airlines')

class AirlinesDeleteView(BSModalDeleteView):
    model = Airlines
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:airlines')
# -------------------------------------------------------------------


# ---------------------------------ВС----------------------
class AirplaneView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/airplane_list.html'
    context_object_name = 'airplane'
    model = Airplane

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Воздушные судна")
        return dict(list(context.items()) + list(c_def.items()))
    
class AirplaneCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = AirplaneModelForm
    success_url = reverse_lazy('timetable:airplane')

class AirplaneUpdateView(BSModalUpdateView):
    model = Airplane
    template_name = 'table_tgo/edit_data/update.html'
    form_class = AirplaneModelForm
    success_url = reverse_lazy('timetable:airplane')

class AirplaneDeleteView(BSModalDeleteView):
    model = Airplane
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:airplane')
# -------------------------------------------------------------------


# ---------------------------------Страны----------------------
class CountryView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/сountry_list.html'
    context_object_name = 'country'
    model = Country

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Страны")
        return dict(list(context.items()) + list(c_def.items()))
    
class CountryCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('timetable:country')

class CountryUpdateView(BSModalUpdateView):
    model = Country
    template_name = 'table_tgo/edit_data/update.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('timetable:country')

class CountryDeleteView(BSModalDeleteView):
    model = Country
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:country')
# -------------------------------------------------------------------


# ---------------------------------Города----------------------
class CityView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/city_list.html'
    context_object_name = 'city'
    model = City

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Города")
        return dict(list(context.items()) + list(c_def.items()))
    
class CityCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = CityModelForm
    success_url = reverse_lazy('timetable:city')

class CityUpdateView(BSModalUpdateView):
    model = City
    template_name = 'table_tgo/edit_data/update.html'
    form_class = CityModelForm
    success_url = reverse_lazy('timetable:city')

class CityDeleteView(BSModalDeleteView):
    model = City
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:city')
# -------------------------------------------------------------------


# ---------------------------------Аэропорты----------------------
class AirportView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/airport_list.html'
    context_object_name = 'airport'
    model = Airport

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Аэропорты")
        return dict(list(context.items()) + list(c_def.items()))
    
class AirportCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = AirportModelForm
    success_url = reverse_lazy('timetable:airport')

class AirportUpdateView(BSModalUpdateView):
    model = Airport
    template_name = 'table_tgo/edit_data/update.html'
    form_class = AirportModelForm
    success_url = reverse_lazy('timetable:airport')

class AirportDeleteView(BSModalDeleteView):
    model = Airport
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:airport')
# -------------------------------------------------------------------


# ---------------------------------Рейсы----------------------
class FlightView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/flight_list.html'
    context_object_name = 'flight'
    model = Flight

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Рейсы")
        return dict(list(context.items()) + list(c_def.items()))
    
class FlightCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = FlightModelForm
    success_url = reverse_lazy('timetable:flight')

class FlightUpdateView(BSModalUpdateView):
    model = Flight
    template_name = 'table_tgo/edit_data/update.html'
    form_class = FlightModelForm
    success_url = reverse_lazy('timetable:flight')

class FlightDeleteView(BSModalDeleteView):
    model = Flight
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:flight')
# -------------------------------------------------------------------


# ---------------------------------Типы рейсов----------------------
class TypeFlightView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/typeFlight_list.html'
    context_object_name = 'typeFligh'
    model = TypeFlight

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Типы рейсов")
        return dict(list(context.items()) + list(c_def.items()))
    
class TypeFlightCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = TypeFlightModelForm
    success_url = reverse_lazy('timetable:type_flight')

class TypeFlightUpdateView(BSModalUpdateView):
    model = TypeFlight
    template_name = 'table_tgo/edit_data/update.html'
    form_class = TypeFlightModelForm
    success_url = reverse_lazy('timetable:type_flight')

class TypeFlightDeleteView(BSModalDeleteView):
    model = TypeFlight
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:type_flight')
# -------------------------------------------------------------------


# ---------------------------------Типы стран----------------------
class TypeCountryView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/typeCountry_list.html'
    context_object_name = 'typeCountry'
    model = TypeCountry

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Типы стран")
        return dict(list(context.items()) + list(c_def.items()))
    
class TypeCountryCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = TypeCountryModelForm
    success_url = reverse_lazy('timetable:type_country')

class TypeCountryUpdateView(BSModalUpdateView):
    model = TypeCountry
    template_name = 'table_tgo/edit_data/update.html'
    form_class = TypeCountryModelForm
    success_url = reverse_lazy('timetable:type_country')

class TypeCountryDeleteView(BSModalDeleteView):
    model = TypeCountry
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:type_country')
# -------------------------------------------------------------------


# ---------------------------------Комплектация ВС----------------------
class EquipmentAirplaneView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/equipmentAirplane_list.html'
    context_object_name = 'EquipmentAirplane'
    model = EquipmentAirplane

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Комплектация ВС")
        return dict(list(context.items()) + list(c_def.items()))
    
class EquipmentAirplaneCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = EquipmentAirplaneModelForm
    success_url = reverse_lazy('timetable:equipmentAirplane')

class EquipmentAirplaneUpdateView(BSModalUpdateView):
    model = EquipmentAirplane
    template_name = 'table_tgo/edit_data/update.html'
    form_class = EquipmentAirplaneModelForm
    success_url = reverse_lazy('timetable:equipmentAirplane')

class EquipmentAirplaneDeleteView(BSModalDeleteView):
    model = EquipmentAirplane
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:equipmentAirplane')
# -------------------------------------------------------------------


# ---------------------------------Статусы рейсов----------------------
class TimetableStatusView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/timetableStatus_list.html'
    context_object_name = 'TimetableStatus'
    model = TimetableStatus

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Статусы рейсов")
        return dict(list(context.items()) + list(c_def.items()))
    
class TimetableStatusCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = TimetableStatusModelForm
    success_url = reverse_lazy('timetable:timetableStatus')

class TimetableStatusUpdateView(BSModalUpdateView):
    model = TimetableStatus
    template_name = 'table_tgo/edit_data/update.html'
    form_class = TimetableStatusModelForm
    success_url = reverse_lazy('timetable:timetableStatus')

class TimetableStatusDeleteView(BSModalDeleteView):
    model = TimetableStatus
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:timetableStatus')    