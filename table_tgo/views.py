
from django.views.generic import ListView
from .models import (TGO_object
                     , RessourceOperation
                     , TGO
                     , delete_TGO
                     )
from django.db.models import Prefetch
from .utils import *

from .forms import (
    TGOModelForm
    , TGO_objectModelForm
    , RessourceOperationModelForm
)

from bootstrap_modal_forms.generic import (
  BSModalCreateView
  , BSModalDeleteView
  , BSModalUpdateView
)
from .cache_query import *
from django.shortcuts import redirect 


class TGOIndex(DataMixin, ListView):
    template_name = 'table_tgo/index.html'
    context_object_name = 'tgo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список ТГО")
        context = dict(list(context.items()) + list(c_def.items()))
        return context
    
    def get_queryset(self):
        return get_tgo()
    

class ShowTGO(DataMixin, ListView):
    template_name = 'table_tgo/data/tgo_objects.html'
    context_object_name = 'tgo_objects'
    model = TGO_object
   
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = title='ТГО ' + self.kwargs['title']
        c_def = self.get_user_context(title=title)
        context = dict(list(context.items()) + list(c_def.items()))
        context['title_TGO'] = self.kwargs['title']
        context['tgo_id'] = self.kwargs['id']
        return context
    
    def get_queryset(self):
        return super(ShowTGO, self).get_queryset().filter(tgo = self.kwargs['id']).select_related().prefetch_related(
            Prefetch(
            'ressource', 
            queryset=RessourceOperation.objects.select_related(),
            ),
        )
    

#-----------------Добавление----------------------
class TgoCreateView(DataMixin, BSModalCreateView):
    template_name = 'table_tgo/edit_data/create.html'
    form_class = TGOModelForm
    success_message = 'Успешно создана новая запись.'
    success_url = reverse_lazy('table_tgo:index')


class TGO_objectCreateView(DataMixin, MySuccesURL, BSModalCreateView):
    form_class = TGO_objectModelForm
    template_name = 'table_tgo/edit_data/create.html'
    success_message = 'Успешно создана новая операция.'
    
    def get_context_data(self, **kwargs):
        context = super(TGO_objectCreateView, self).get_context_data(**kwargs)
        context['form'] = TGO_objectModelForm(
        initial={
        'tgo': self.request.resolver_match.kwargs['tgo_id'],
        })
        return context  


class ResourceCreateView(DataMixin, MySuccesURL, BSModalCreateView):
    form_class = RessourceOperationModelForm
    template_name = 'table_tgo/edit_data/create.html'
    success_message = 'Успешно создан новый ресурс.'
    
    def get_context_data(self, **kwargs):
        context = super(ResourceCreateView, self).get_context_data(**kwargs)
        context['form'] = RessourceOperationModelForm(
        initial={
        'tgo': self.request.resolver_match.kwargs['tgo_id'],
        'tgo_object': self.request.resolver_match.kwargs['tgo_object_id'],
        }
        )
        return context
#-----------------Добавление КОНЕЦ----------------------


#-----------------Обновление----------------------
class TGOUpdateView(BSModalUpdateView):
    model = TGO
    template_name = 'table_tgo/edit_data/update.html'
    form_class = TGOModelForm
    success_message = 'Запись успешно обновлена'
    success_url = reverse_lazy('table_tgo:index')

class TGO_objectUpdateView(MySuccesURL, BSModalUpdateView):
    model = TGO_object
    template_name = 'table_tgo/edit_data/update.html'
    form_class = TGO_objectModelForm
    success_message = 'Запись успешно обновлена'
    

class ResourceUpdateView(MySuccesURL, BSModalUpdateView):
    model = RessourceOperation
    template_name = 'table_tgo/edit_data/update.html'
    form_class = RessourceOperationModelForm
    success_message = 'Запись успешно обновлена'
#-----------------Обновление КОНЕЦ----------------------    


#-----------------Удаление ----------------------    
class TGO_objectDeleteView(MySuccesURL, BSModalDeleteView):
    model = TGO_object
    template_name = 'table_tgo/edit_data/delete.html'
    success_message = 'ТГО успешно удален'

    def get_success_url(self):
        tgo_id = self.object.tgo.id
        tgo_title = self.object.tgo.title
        return reverse_lazy('table_tgo:tgo_objects', kwargs={'id': tgo_id, 'title': tgo_title})


class ResourceDeleteView(MySuccesURL, BSModalDeleteView):
    model = RessourceOperation
    template_name = 'table_tgo/edit_data/delete.html'
    success_message = 'Ресурс успешно удален'
#-----------------Удаление КОНЕЦ----------------------    




#-----------------Обновление БД через Ajax ----------------------    
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction

#Обновляем время у одного ТГО
@login_required
@csrf_exempt
def update_tgo(request):
    data = dict()
    update_tgoObj_arr = []
    update_res_arr = [] 
    
    for i,j in request.POST.items():
            if request.POST.getlist(i)[0] == 'table_tgo_tgo_object':
                update_tgoObj_arr.append(request.POST.getlist(i))
            if request.POST.getlist(i)[0] == 'table_tgo_ressourceoperation':
                update_res_arr.append(request.POST.getlist(i))

    #получаем списки с id и значениями которые нужно обновить для двух таблиц
    [update_res_arr[i].pop(0) for i in range(len(update_res_arr))]
    [update_tgoObj_arr[i].pop(0) for i in range(len(update_tgoObj_arr))]  
    
    with transaction.atomic():
        for elem in update_tgoObj_arr:
            TGO_object.objects.filter(id=elem[0]).update(time_start=elem[1], time_lenght=elem[2], time_end=elem[3])

    with transaction.atomic():
        for elem in update_res_arr:
            RessourceOperation.objects.filter(id=elem[0]).update(time_start=elem[1], time_lenght=elem[2], time_end=elem[3])
            
    return JsonResponse(data)
#-----------------Обновление БД через Ajax конец----------------------    


#Копируем ТГО
@login_required
def copy_tgo(request, pk):
    instance = TGO.objects.get(pk = pk)
    old_tgo_objects = TGO_object.objects.filter(tgo = instance.pk)
    
    instance.pk = None
    instance.title = 'копия_' + instance.title
    instance.save()

    for tgo_obj in old_tgo_objects:
        tgo_obj.pk = None
        tgo_obj.tgo = instance
        tgo_obj.time_start ='0'
        tgo_obj.time_lenght = '0'
        tgo_obj.time_end = '0'
        tgo_obj.save()

    #очищаем кэш   
    delete_TGO() 
    return redirect('table_tgo:index')


