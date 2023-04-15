from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from table.models import ScheduleNotJob
from django.http import HttpResponse


def index(request, user):
    try:
        EditorPremission(user)
        return HttpResponse("yea")
    except:
        return HttpResponse("oops.. no")


def EditorPremission(user):
   # editor_group, created = Group.objects.get_or_create(name="Editor")

    content_type = ContentType.objects.get_for_model(ScheduleNotJob)
    post_permission = Permission.objects.filter(content_type=content_type)
   # print([perm.codename for perm in post_permission]) 
   # ['add_schedulenotjob', 'change_schedulenotjob', 'delete_schedulenotjob', 'view_schedulenotjob']
    
'''
    for perm in post_permission:
        if perm.codename == "add_place":
            editor_group.permissions.add(perm)
        elif perm.codename == "view_place":
            editor_group.permissions.add(perm)


    user = User.objects.get(username=user)
    user.groups.add(editor_group)

    user = get_object_or_404(User, pk=user.id)

    print(user.has_perm("place.delete_place")) 
    print(user.has_perm("place.change_place")) 
    print(user.has_perm("place.view_place")) 
    print(user.has_perm("place.add_place"))
'''
#https://testdriven.io/blog/django-permissions/