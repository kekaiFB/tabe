
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.views.generic import TemplateView
from .models import *
from .utils import *
from .forms import *
from django.http import HttpResponseRedirect
from bootstrap_modal_forms.generic import (
   BSModalCreateView
  , BSModalDeleteView
  , BSModalUpdateView
)
from django.contrib.auth.decorators import login_required
from .templatetags.timetable_tags import timetable_history_tag

from django.http import JsonResponse

# ---------------------------------Расписания----------------------
class TimetableListView(DataMixin, MyModel, ListView):
    template_name = 'timetable/index_list.html'
    context_object_name = 'TimetableList'
    model = TimetableList

    def get_queryset(self):
        return super(TimetableListView, self).get_queryset().select_related()
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = title='Расписания'
        c_def = self.get_user_context(title=title)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class TimetableListCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = TimetableListModelForm
    success_url = reverse_lazy('timetable:timetable_list')
    
    def form_valid(self, form):
        self.instance = form.save(commit=False)
        self.instance.author = self.request.user 
        return super().form_valid(form)


@login_required
def load_ajax_fligh_data(request):
    flight_type = ''
    data = {}
   
    id_flight = '' if not request.GET.get('id_flight') else str(request.GET.get('id_flight'))
    
    if id_flight != '':
      flight_type =  Flight.objects.filter(id=id_flight).values('type_flight')[0]

    if flight_type:
        data['flight_type'] = flight_type

    return JsonResponse(data)

class TimetableListUpdateView(DetailView, BSModalUpdateView):
    model = TimetableList
    template_name = 'table_tgo/edit_data/update.html'
    form_class = TimetableListModelForm
    success_url = reverse_lazy('timetable:timetable_list')


class TimetableListDeleteView(BSModalDeleteView):
    model = TimetableList
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:timetable_list')


#Копируем ТГО (Полная копия) 
@login_required
def copy_timetable(request, pk):
    instance = TimetableList.objects.get(pk = pk)
    old_timetable = Timetable.objects.filter(timetablelist = instance.pk)

    instance.pk = None
    instance.title = 'копия_' + instance.title
    instance.author = request.user
    instance.save()

    for timetable_obj in old_timetable:
        timetable_obj.pk = None
        timetable_obj.author = request.user
        timetable_obj.editor = request.user
        timetable_obj.timetablelist = instance
        timetable_obj.save()

    return HttpResponseRedirect(reverse('timetable:timetable_list'))
# -------------------------------------------------------------------


# ---------------------------------Расписание----------------------
class TimeTableView(DataMixin, MyModel, TemplateView):
    template_name = 'timetable/index_standart.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=self.kwargs['title'])
        context = dict(list(context.items()) + list(c_def.items()))

        #Делаем оосновной queryset + th для истории изменения
        t = Timetable.objects.filter(timetablelist = self.kwargs['id']).select_related()
        th = timetable_history_tag(t)
        context['timetable'] = zip(t, th)

        context['title_timetable'] = self.kwargs['title']
        context['timetable_id'] = self.kwargs['id']

        #Для дней недели
        days_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        context['days_week'] = days_week
        author = None if not self.request.POST.get('author') else str(self.request.POST.get('author'))
        if author:
            context['author'] = author
        
        return context
        
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
          

class TimeTableCreateView(MySuccesURL, DataMixin, BSModalCreateView):
    template_name = 'timetable/edit_data/createTimeTable.html'
    form_class = TimeTableModelForm

    def get_context_data(self, **kwargs):
        context = super(TimeTableCreateView, self).get_context_data(**kwargs)
        context['form'] = TimeTableModelForm(
        initial={
        'timetablelist': self.request.resolver_match.kwargs['timetable_id'],
        })
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        req_user = self.request.user
        if str(instance.timetablelist.author) == str(req_user): 
            instance = form.save(commit=False)
            instance.author = req_user
            instance.editor = req_user
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")  



class TimeTableUpdateView(MySuccesURL, BSModalUpdateView):
    model = Timetable
    context_object_name = 'timetable'
    template_name = 'timetable/edit_data/updateTimetable.html'
    form_class = TimeTableModelForm

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        if str(self.instance.author) == str(self.request.user): 
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")

class TimeTableDeleteView(MySuccesURL, BSModalDeleteView):
    model = Timetable
    template_name = 'table_tgo/edit_data/delete.html'

    def form_valid(self, form):
        self.object = self.get_object()
        if str(self.object.author) != str(self.request.user): 
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")
        else:
            return super(TimeTableDeleteView, self).form_valid(form)
# -------------------------------------------------------------------


# ---------------------------------Недельное расписание----------------------
class TimeTableWeekView(DataMixin, MyModel, TemplateView):
    template_name = 'timetable/index_week.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=self.kwargs['title'])
        context = dict(list(context.items()) + list(c_def.items()))

        #Делаем оосновной queryset + th для истории изменения
        t = Timetable.objects.filter(timetablelist = self.kwargs['id']).select_related()
        th = timetable_history_tag(t)
        context['timetable'] = zip(t, th)

        context['title_timetable'] = self.kwargs['title']
        context['timetable_id'] = self.kwargs['id']

        #Для дней недели
        days_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        context['days_week'] = days_week
        author = None if not self.request.POST.get('author') else str(self.request.POST.get('author'))
        if author:
            context['author'] = author
        
        return context
        
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
          

class TimeTableWeekCreateView(MySuccesURLWeek, DataMixin, BSModalCreateView):
    template_name = 'timetable/edit_data/createTimeTable.html'
    form_class = TimeTableModelForm

    def get_context_data(self, **kwargs):
        context = super(TimeTableWeekCreateView, self).get_context_data(**kwargs)
        context['form'] = TimeTableModelForm(
        initial={
        'timetablelist': self.request.resolver_match.kwargs['timetable_id'],
        })
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        req_user = self.request.user
        if str(instance.timetablelist.author) == str(req_user): 
            instance = form.save(commit=False)
            instance.author = req_user
            instance.editor = req_user
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")  


class TimeTableWeekUpdateView(MySuccesURLWeek, BSModalUpdateView):
    model = Timetable
    context_object_name = 'timetable'
    template_name = 'timetable/edit_data/updateTimeTable.html'
    form_class = TimeTableModelForm

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        if str(self.instance.author) == str(self.request.user): 
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")

class TimeTableWeekDeleteView(MySuccesURLWeek, BSModalDeleteView):
    model = Timetable
    template_name = 'table_tgo/edit_data/delete.html'

    def form_valid(self, form):
        self.object = self.get_object()
        if str(self.object.author) != str(self.request.user): 
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")
        else:
            return super(TimeTableWeekDeleteView, self).form_valid(form)
# -------------------------------------------------------------------


# ---------------------------------Сгруппированное недельное расписание----------------------
class TimeTableWeekGroupView(DataMixin, MyModel, TemplateView):
    template_name = 'timetable/index_week_group.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=self.kwargs['title'])
        context = dict(list(context.items()) + list(c_def.items()))

        #Делаем оосновной queryset + th для истории изменения
        t = Timetable.objects.filter(timetablelist = self.kwargs['id']).select_related()
        th = timetable_history_tag(t)
        context['timetable'] = zip(t, th)

        context['title_timetable'] = self.kwargs['title']
        context['timetable_id'] = self.kwargs['id']

        #Для дней недели
        days_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        context['days_week'] = days_week
        author = None if not self.request.POST.get('author') else str(self.request.POST.get('author'))
        if author:
            context['author'] = author
        
        return context
       
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
          

class TimeTableWeekGroupCreateView(MySuccesURLWeekGroup, DataMixin, BSModalCreateView):
    template_name = 'timetable/edit_data/createTimeTable.html'
    form_class = TimeTableModelForm

    def get_context_data(self, **kwargs):
        context = super(TimeTableWeekGroupCreateView, self).get_context_data(**kwargs)
        context['form'] = TimeTableModelForm(
        initial={
        'timetablelist': self.request.resolver_match.kwargs['timetable_id'],
        })
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        req_user = self.request.user
        if str(instance.timetablelist.author) == str(req_user): 
            instance = form.save(commit=False)
            instance.author = req_user
            instance.editor = req_user
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")  



class TimeTableWeekGroupUpdateView(MySuccesURLWeekGroup, BSModalUpdateView):
    model = Timetable
    context_object_name = 'timetable'
    template_name = 'timetable/edit_data/updateTimeTable.html'
    form_class = TimeTableModelForm

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        if str(self.instance.author) == str(self.request.user): 
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")

class TimeTableWeekGroupDeleteView(MySuccesURLWeekGroup, BSModalDeleteView):
    model = Timetable
    template_name = 'table_tgo/edit_data/delete.html'

    def form_valid(self, form):
        self.object = self.get_object()
        if str(self.object.author) != str(self.request.user): 
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")
        else:
            return super(TimeTableWeekGroupDeleteView, self).form_valid(form)
# -------------------------------------------------------------------


# ---------------------------------Авиакомпании----------------------
class AirlinesView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/airlines_list.html'
    context_object_name = 'airlines'
    model = Airlines

    def get_queryset(self):
        return super(AirlinesView, self).get_queryset().select_related()

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

    def get_queryset(self):
        return super(AirplaneView, self).get_queryset().select_related()

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

    def get_queryset(self):
        return super(CountryView, self).get_queryset().select_related()

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

    def get_queryset(self):
        return super(CityView, self).get_queryset().select_related()

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

    def get_queryset(self):
        return super(AirportView, self).get_queryset().select_related()

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

    def get_queryset(self):
        return super(FlightView, self).get_queryset().select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Рейсы")
        return dict(list(context.items()) + list(c_def.items()))
    
class FlightCreateView(DataMixin, BSModalCreateView):
    template_name = 'timetable/edit_data/createFlight.html'
    form_class = FlightModelForm
    success_url = reverse_lazy('timetable:flight')
    
    

class FlightUpdateView(BSModalUpdateView):
    model = Flight
    template_name = 'timetable/edit_data/updateFlight.html'
    form_class = FlightModelForm
    success_url = reverse_lazy('timetable:flight')

    
class FlightDeleteView(BSModalDeleteView):
    model = Flight
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('timetable:flight')



# ---------------------------------Типы рейсов----------------------
class TypeFlightView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/typeFlight_list.html'
    context_object_name = 'typeFligh'
    model = TypeFlight

    def get_queryset(self):
        return super(TypeFlightView, self).get_queryset().select_related()


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

    def get_queryset(self):
        return super(TypeCountryView, self).get_queryset().select_related()

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

    def get_queryset(self):
        return super(EquipmentAirplaneView, self).get_queryset().select_related()

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

    def get_queryset(self):
        return super(TimetableStatusView, self).get_queryset().select_related()

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
# -------------------------------------------------------------------


# ---------------------------------История одного расписания----------------------
class HistoryTimetableView(DataMixin, MyModel, ListView):
    template_name = 'timetable/models/history/history_timetableObjects_list.html'
    context_object_name = 'timetable'
    model = Timetable

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = title='Контроль версий '
        c_def = self.get_user_context(title=title)
        context = dict(list(context.items()) + list(c_def.items()))
        context['timetable_id'] = self.kwargs['id']
        return context
    
    def get_queryset(self):
        return super(HistoryTimetableView, self).get_queryset().get(id = self.kwargs['id']).history.select_related('flight', 'airline', 'timetablestatusight', 'tgo', 'author').order_by('-history_date')


@login_required
def editHistoryObject(request, pk,  history_id):  
    if request.method == 'POST':
        author = None if not request.POST.get('author') else str(request.POST.get('author'))
        req_user = request.user
        if str(author) == str(req_user): 
            elem = Timetable.objects.filter(id = pk)[0].history.select_related('flight', 'airline', 'timetablestatusight', 'tgo', 'author')
            elem.filter(history_id = history_id)[0].instance.save()
            elem.filter(history_id = history_id).delete()

            return HttpResponseRedirect(reverse(
            'timetable:historyTimetable',
                kwargs={
                    'id': pk
                }
            ))
        else:
            print(forms.ValidationError(u"Вы не явялетесь владельцем этой записи"))
            return HttpResponseRedirect(reverse(
            'timetable:historyTimetable',
                kwargs={
                    'id': pk
                }
            ))


class HistoryTimetableDeleteView(BSModalDeleteView):
    model = Timetable
    template_name = 'table_tgo/edit_data/delete.html'

    def form_valid(self, form):
        author = None if not self.request.POST.get('author') else str(self.request.POST.get('author'))
        req_user = self.request.user

        if str(author) == str(req_user):
            self.instance = form.save(commit=False)
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.history.filter(history_id = self.kwargs['history_id']).delete()
            return HttpResponseRedirect(success_url)
        else:
            print(forms.ValidationError(u"Вы не явялетесь владельцем этой записи"))
            return HttpResponseRedirect(reverse(
            'timetable:historyTimetable',
                kwargs={
                    'id': self.kwargs['pk']
                }
            ))
    
    def get_success_url(self):
        return reverse(
            'timetable:historyTimetable',
            kwargs={
                'id': self.object.id
            }
        )