from django.contrib import admin
from .models import (Human
                     , Post
                     , Office
                     , Reason
                     , Shift
                     , ScheduleNotJob)


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title',)
    
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'office', 'title',)
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'office__title', 'title',)

class HumanAdmin(admin.ModelAdmin):
    list_display = ('id', 'office', 'post', 'initials',)
    list_display_links = ('id', 'initials',)
    search_fields = ('id', 'office__title', 'post__title', 'initials',)
    
class ReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'digital_code', 'character_code',)
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title', 'digital_code', 'character_code',)

class ShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title', 'description')

class ScheduleNotJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'shift', 'office', 'post', 'human', 
                    'reason', 'comment', 'length_time', 'date_start', 'date_end',)
    list_display_links = ('id', 'human',)
    search_fields = ('id', 'shift', 'office__title', 
                     'post__title', 'human__initials', 
                     'reason__title', 'comment', 'length_time', 
                     'date_start', 'date_end',)


admin.site.register(Office, OfficeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Human, HumanAdmin)
admin.site.register(Reason, ReasonAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(ScheduleNotJob, ScheduleNotJobAdmin)

#pip install django-smart-selects