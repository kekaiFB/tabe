from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django import forms


class DataMixin(LoginRequiredMixin):
    login_url = reverse_lazy('user:login')

    def get_user_context(self, **kwargs):
        context = kwargs
        return context
    
class MySuccesURL(LoginRequiredMixin):
    def get_success_url(self):
        tgo_id = self.object.tgo.id
        tgo_title = self.object.tgo.title
        return reverse_lazy('table_tgo:tgo_objects', kwargs={'id': tgo_id, 'title': tgo_title})
    

              