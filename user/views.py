from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import RegisterUserForm, LoginForm
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model

from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes  
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token 
from django.core.mail import EmailMessage  
  

def registerUserForm(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Активируйте учетную запись'
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            message = 'Проверьте электронную почту чтобы завершить регистрацию'
            return render(request, 'user/message.html', {'message': message})
    else:
        form = RegisterUserForm()
    return render(request, 'user/register.html', {'form': form})


class LoginUser(TemplateView, LoginView):
    form = LoginForm
    template_name = 'user/login.html'
    success_message = 'Success: You were successfully logged in.'
    extra_context = dict(success_url=reverse_lazy('table:index'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        return context


def logout_user(request):
    logout(request)
    return redirect('user:login')


class ErrorHandler(TemplateView):
    error_code = 404
    template_name = 'user/error.html'

    def dispatch(self, request, *args, **kwargs):
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
    


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        message = 'Спасибо за подтверждение по электронной почте. Теперь вы можете войти в свою учетную запись.'
        return render(request, 'user/message.html', {'message': message})
    else:
        message = 'Ссылка активации недействительна!'
        return render(request, 'user/message.html', {'message': message})  
