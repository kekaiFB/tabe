'''
from django.views.generic import ListView
from .models import (TGO_object
                     , RessourceOperation
                     , TGO
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

from django.shortcuts import redirect 


class TGOIndex(DataMixin, ListView):
    template_name = 'table_tgo/index.html'
    context_object_name = 'tgo'
    model = TGO

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список ТГО")
        context = dict(list(context.items()) + list(c_def.items()))

        author = None if not self.request.POST.get('author') else str(self.request.POST.get('author'))
        if author:
            if str(self.request.user) ==  author:
                context['filter'] = 'my'
            else:
                context['filter'] = 'all'
        else:
            filter = self.request.GET.get('select')
            context['filter'] = 'my'
            if filter == 'all':
                context['filter'] = 'all'
        return context


    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

    def get_queryset(self):
        filter = self.request.GET.get('select')
        
        author = None if not self.request.POST.get('author') else str(self.request.POST.get('author'))
        if author:
            if str(self.request.user) ==  author:
                filter = 'my'
            else:
                filter = 'all'

        if filter == 'all':
            qs = self.model.objects.select_related()
        else:
            qs = self.model.objects.filter(author=self.request.user).select_related()
        return qs
    

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
    success_url = reverse_lazy('table_tgo:index')
    
    def form_valid(self, form):
        self.instance = form.save(commit=False)
        self.instance.author = self.request.user 
        return super().form_valid(form)



class TGO_objectCreateView(DataMixin, MySuccesURL, BSModalCreateView):
    form_class = TGO_objectModelForm
    template_name = 'table_tgo/edit_data/create.html'
    
    def get_context_data(self, **kwargs):
        context = super(TGO_objectCreateView, self).get_context_data(**kwargs)
        context['form'] = TGO_objectModelForm(
        initial={
        'tgo': self.request.resolver_match.kwargs['tgo_id'],
        })
        return context

    
    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.tgo.author == self.request.user: 
            instance = form.save(commit=False)
            instance.author = self.request.user 
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")  
  


class ResourceCreateView(DataMixin, MySuccesURL, BSModalCreateView):
    form_class = RessourceOperationModelForm
    template_name = 'table_tgo/edit_data/create.html'
    
    def get_context_data(self, **kwargs):
        context = super(ResourceCreateView, self).get_context_data(**kwargs)
        context['form'] = RessourceOperationModelForm(
        initial={
        'tgo': self.request.resolver_match.kwargs['tgo_id'],
        'tgo_object': self.request.resolver_match.kwargs['tgo_object_id'],
        }
        )
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.tgo.author == self.request.user:
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")
#-----------------Добавление КОНЕЦ----------------------


#-----------------Обновление----------------------
class TGOUpdateView(BSModalUpdateView):
    model = TGO
    template_name = 'table_tgo/edit_data/update.html'
    form_class = TGOModelForm
    success_url = reverse_lazy('table_tgo:index')

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        if self.instance.author == self.request.user: 
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")
    

class TGO_objectUpdateView(MySuccesURL, BSModalUpdateView):
    model = TGO_object
    template_name = 'table_tgo/edit_data/update.html'
    form_class = TGO_objectModelForm

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        if self.instance.author == self.request.user: 
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")
        
    

class ResourceUpdateView(MySuccesURL, BSModalUpdateView):
    model = RessourceOperation
    template_name = 'table_tgo/edit_data/update.html'
    form_class = RessourceOperationModelForm

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        if self.instance.tgo.author == self.request.user: 
            return super().form_valid(form)
        else:
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")
#-----------------Обновление КОНЕЦ----------------------    



#-----------------Удаление ----------------------   
class TGODeleteView(BSModalDeleteView):
    model = TGO
    template_name = 'table_tgo/edit_data/delete.html'
    success_url = reverse_lazy('table_tgo:index')

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.author != self.request.user: 
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")
        else:
            return super(TGODeleteView, self).form_valid(form)

    
class TGO_objectDeleteView(MySuccesURL, BSModalDeleteView):
    model = TGO_object
    template_name = 'table_tgo/edit_data/delete.html'

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.author != self.request.user: 
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")
        else:
            return super(TGO_objectDeleteView, self).form_valid(form)


class ResourceDeleteView(MySuccesURL, BSModalDeleteView):
    model = RessourceOperation
    template_name = 'table_tgo/edit_data/delete.html'

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.tgo.author != self.request.user: 
            raise forms.ValidationError(u"Вы не явялетесь владельцем этой записи")
        else:
            return super(ResourceDeleteView, self).form_valid(form)
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
            if request.POST.getlist(i)[1] == 'table_tgo_tgo_object':
                update_tgoObj_arr.append(request.POST.getlist(i))
            if request.POST.getlist(i)[1] == 'table_tgo_ressourceoperation':
                update_res_arr.append(request.POST.getlist(i))

    #получаем списки с id и значениями которые нужно обновить для двух таблиц
    author = update_res_arr[0][2]
    [update_res_arr[i].pop(1) for i in range(len(update_res_arr))]
    [update_tgoObj_arr[i].pop(1) for i in range(len(update_tgoObj_arr))]  
    [update_res_arr[i].pop(1) for i in range(len(update_res_arr))]
    [update_tgoObj_arr[i].pop(1) for i in range(len(update_tgoObj_arr))]  

    if str(request.user) == str(author):
        with transaction.atomic():
            for elem in update_tgoObj_arr:
                TGO_object.objects.filter(id=elem[0]).update(time_start=elem[1], time_end=elem[2], time_lenght=elem[3])
                
            for elem in update_res_arr:
                RessourceOperation.objects.filter(id=elem[0]).update(time_start=elem[1], time_end=elem[2], time_lenght=elem[3])
    else:
        print('Вы не являетесь владельцом этой записи')
            
    return JsonResponse(data)
#-----------------Обновление БД через Ajax конец----------------------    


#Копируем ТГО (только операции)
@login_required
def copy_tgo(request, pk):
    instance = TGO.objects.get(pk = pk)
    old_tgo_objects = TGO_object.objects.filter(tgo = instance.pk)
    
    instance.pk = None
    instance.author = request.user
    instance.title = 'копия_' + instance.title
    instance.save()

    for tgo_obj in old_tgo_objects:
        tgo_obj.pk = None
        tgo_obj.author = request.user
        tgo_obj.tgo = instance
        tgo_obj.time_start ='0'
        tgo_obj.time_lenght = '0'
        tgo_obj.time_end = '0'
        tgo_obj.save()

    return redirect('table_tgo:index')


#Копируем ТГО (Полная копия) 
@login_required
def copy_tgo_all(request, pk):
    instance = TGO.objects.get(pk = pk)
    old_tgo_objects = TGO_object.objects.filter(tgo = instance.pk)
    res_objects = RessourceOperation.objects.filter(tgo = instance.pk)
    
    instance.pk = None
    instance.title = 'полная_копия_' + instance.title
    instance.author = request.user
    instance.save()

    for tgo_obj in old_tgo_objects:
        current_tgo = tgo_obj.id
        tgo_obj.pk = None
        tgo_obj.author = request.user
        tgo_obj.tgo = instance
        tgo_obj.save()

        for res_obj in res_objects:
            if res_obj.tgo_object.id == current_tgo:
                print(1)
                res_obj.pk = None
                res_obj.tgo = instance
                res_obj.tgo_object = tgo_obj
                res_obj.save()

    return redirect('table_tgo:index')

'''