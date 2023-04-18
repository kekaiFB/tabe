from django.contrib import admin
from .models import (Operation
                     , Ressource
                     , TGO_object
                     , RessourceOperation
                     , TGO
                     )
from django.contrib import admin


class RessourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'office',)
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title', 'office',)


# class TGOAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'tgo_detail',)
#     list_display_links = ('id', 'title',)
#     search_fields = ('id', 'title', 'tgo_detail',)
    
#     def tgo_detail(self,obj):
#         tgo_detail = [elem.id for elem in TGO_object.objects.filter(tgo = obj.id)]
#         return list(list([RessourceOperation.objects.filter(tgo_object = elem) for elem in tgo_detail]))


# class TGO_objectAdmin(admin.ModelAdmin):
#     list_display = ('id', 'tgo', 'operation',)
#     list_display_links = ('id', 'operation',)
#     search_fields = ('id', 'tgo', 'operation',)


# class RessourceOperationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'tgo', 'tgo_object', 'ressource', 'count',)
#     list_display_links = ('id', 'tgo_object',)
#     search_fields = ('id', 'tgo', 'tgo_object', 'ressource', 'count',)

#     def get_ressource(self,obj):
#         return [ressource.title for ressource in obj.ressource.all()]
    

admin.site.register(Operation, )
admin.site.register(Ressource, RessourceAdmin)
# admin.site.register(TGO, TGOAdmin)
# admin.site.register(TGO_object, TGO_objectAdmin)
# admin.site.register(RessourceOperation, RessourceOperationAdmin)