from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render  
from .forms import SNJ  
from .models import ScheduleNotJob, Office, Human, Post  
from django.http import JsonResponse
from django.template.loader import render_to_string 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.cache import cache



@login_required
def load_ajax_form(request):
    data = dict()

    offices = None
    posts = None
    humans = None

    id_office = 0 if not request.GET.get('id_office') else int(request.GET.get('id_office'))
    id_post= 0 if not request.GET.get('id_post') else int(request.GET.get('id_post'))
    id_human = 0 if not request.GET.get('id_human') else int(request.GET.get('id_human'))
    click = request.GET.get('click')

    if click == 'id_office':
        if id_office > 0:
            if id_post > 0:
                if id_human > 0: 
                    pass
                else:
                    humans = Human.objects.filter(office_id=id_office, post_id=id_post).order_by('initials')
            else: 
                if id_human > 0:
                    posts = Post.objects.filter(office_id=id_office, human__id=id_human).order_by('title')
                else:
                    posts = Post.objects.filter(office_id=id_office).order_by('title')
                    humans = Human.objects.filter(office_id=id_office).order_by('initials')
        else: 
            if id_post > 0:
                if id_human > 0: 
                    offices = Office.objects.filter(post__id=id_post, human__id=id_human).order_by('title')
                else:
                    offices = Office.objects.filter(post__id=id_post).order_by('title')
                    humans = Human.objects.filter(post_id=id_post).order_by('initials')
            else: 
                if id_human > 0:
                    offices = Office.objects.filter(human__id=id_human).order_by('title')
                    posts = Post.objects.filter(human__id=id_human).order_by('title')
                else:
                    offices = Office.objects.all()
                    posts = Post.objects.all()
                    humans = Human.objects.all()

    elif click == 'id_post':
        if id_post > 0:
            if id_office > 0:
                if id_human > 0: 
                    pass
                else:
                    humans = Human.objects.filter(office_id=id_office, post_id=id_post).order_by('initials')
            else: 
                if id_human > 0:
                    offices = Office.objects.filter(post__id=id_post, human__id=id_human).order_by('title')
                else:
                    offices = Office.objects.filter(post__id=id_post).order_by('title')
                    humans = Human.objects.filter(post_id=id_post).order_by('initials')
        else: 
            if id_office > 0:
                if id_human > 0: 
                    posts = Post.objects.filter(office_id=id_office, human__id=id_human).order_by('title')
                else:
                    posts = Post.objects.filter(office_id=id_office).order_by('title')
                    humans = Human.objects.filter(office_id=id_office).order_by('initials')
            else: 
                if id_human > 0:
                    offices = Office.objects.filter(human__id=id_human).order_by('title')
                    posts = Post.objects.filter(human__id=id_human).order_by('title')
                else:
                    offices = Office.objects.all()
                    posts = Post.objects.all()
                    humans = Human.objects.all()

    elif click == 'id_human':
        if id_human > 0:
            if id_office > 0:
                if id_post > 0: 
                    pass
                else:
                    posts = Post.objects.filter(office_id=id_office, human__id=id_human).order_by('title')
            else: 
                if id_post > 0:
                    offices = Office.objects.filter(post__id=id_post, human__id=id_human).order_by('title')
                else:
                    offices = Office.objects.filter(human__id=id_human).order_by('title')
                    posts = Post.objects.filter(human__id=id_human).order_by('title')
        else: 
            if id_office > 0:
                if id_post > 0: 
                    humans = Human.objects.filter(office_id=id_office, post_id=id_post).order_by('initials')
                else:
                    posts = Post.objects.filter(office_id=id_office).order_by('title')
                    humans = Human.objects.filter(office_id=id_office).order_by('initials')
            else: 
                if id_post > 0:
                    offices = Office.objects.filter(post__id=id_post).order_by('title')
                    humans = Human.objects.filter(post_id=id_post).order_by('initials')
                else:
                    offices = Office.objects.all()
                    posts = Post.objects.all()
                    humans = Human.objects.all()

    if offices:     
        data['html_office'] = render_to_string('ajax/office.html', { 'offices': offices})
    if humans:     
        data['html_human'] = render_to_string('ajax/human.html', { 'humans': humans})
    if posts:     
        data['html_post'] = render_to_string('ajax/post.html', { 'posts': posts})

    return JsonResponse(data)

def get_snf():
    snj = cache.get('snj')
    if snj is None:
        snj = ScheduleNotJob.objects.select_related()
        cache.set('snj', snj, 300)
    return snj 


@login_required
def index(request):  
    snj = get_snf()
    return render(request,"index.html",{'snj': snj})  


@login_required
def save_product_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':  
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            snj = get_snf()
            data['html_product_list'] = render_to_string('table.html', {
                'snj': SNJ
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def addnew(request):
    if request.method == 'POST':
        form = SNJ(request.POST)
    else:
        form = SNJ()
    return save_product_form(request, form, 'addnew.html')  


@login_required
@permission_required('change_schedulenotjob')
def edit(request, id):
    elem = ScheduleNotJob.objects.prefetch_related().get(pk=id)
    if request.method == "POST":
        form = SNJ(request.POST, instance=elem)
    else:  
        form = SNJ(instance=elem)
    return save_product_form(request, form, 'edit.html')


@login_required
def destroy(request, id):  
    snj = ScheduleNotJob.objects.get(id=id)  
    snj.delete()  
    return HttpResponseRedirect(reverse('table:index'))  
