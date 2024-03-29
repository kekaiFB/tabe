from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django import forms


class DataMixin(LoginRequiredMixin):
    login_url = reverse_lazy('user:login')
    
    def get_user_context(self, **kwargs):
        context = kwargs
        context['prev_url'] = self.request.META.get('HTTP_REFERER')
        return context

class MySuccesURL(LoginRequiredMixin):
    def get_success_url(self):
        id = self.object.timetablelist.id
        title = self.object.timetablelist.title
        return reverse_lazy('timetable:index', kwargs={'id': id, 'title': title})
    

class MySuccesURLWeek(LoginRequiredMixin):
    def get_success_url(self):
        id = self.object.timetablelist.id
        title = self.object.timetablelist.title
        return reverse_lazy('timetable:index_week', kwargs={'id': id, 'title': title})
    

class MySuccesURLWeekGroup(LoginRequiredMixin):
    def get_success_url(self):
        id = self.object.timetablelist.id
        title = self.object.timetablelist.title
        return reverse_lazy('timetable:index_week_group', kwargs={'id': id, 'title': title})


menu = [{'title': "Авиакомпании", 'url_name': 'timetable:airlines'},
        {'title': "Воздушные судна", 'url_name': 'timetable:airplane'},
        {'title': "Страны", 'url_name': 'timetable:country'},
        {'title': "Города", 'url_name': 'timetable:city'},
        {'title': "Аэропорты", 'url_name': 'timetable:airport'},
        {'title': "Рейсы", 'url_name': 'timetable:flight'}
]


class MyModel(LoginRequiredMixin):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context