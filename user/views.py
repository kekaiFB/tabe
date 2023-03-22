from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import CustomRegistrationForm, CustomAuthenticationForm
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from bootstrap_modal_forms.generic import (
  BSModalCreateView,
  BSModalLoginView,
  BSModalReadView
)
from django.contrib.auth.decorators import permission_required


class RegistrationUser(BSModalCreateView):
    form_class = CustomRegistrationForm
    template_name = 'user/registration.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('table:index')

    
class LoginUser(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'user/login.html'
    success_message = 'Success: You were successfully logged in.'
    extra_context = dict(success_url=reverse_lazy('table:index'))


def logout_user(request):
    logout(request)
    return redirect('table:index')



class ErrorHandler(TemplateView):
    error_code = 404
    template_name = 'user/error.html'

    def dispatch(self, request, *args, **kwargs):
        """ For error on any methods return just GET """
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.error_code
        context['error_code'] = self.error_code
        context['kwargs'] = self.kwargs
        return context

    def render_to_response(self, context, **response_kwargs):
        """ Return correct status code """
        response_kwargs = response_kwargs or {}
        response_kwargs.update(status=self.error_code)
        return super().render_to_response(context, **response_kwargs)