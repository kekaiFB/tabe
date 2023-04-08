from django.urls import path
from .views import *

app_name = 'table_tgo'

urlpatterns = [
    path('', TGOIndex.as_view(), name='index'),
    path("tgo/<str:title>/<int:id>/", ShowTGO.as_view(), name='tgo_objects'),

    path('create/', TgoCreateView.as_view(), name='create_tgo'),
    path('create_tgo_object/<int:tgo_id>/', TGO_objectCreateView.as_view(), name='create_tgo_object'),
    path('create_tgo_object_resource/<int:tgo_id>/<int:tgo_object_id>/', ResourceCreateView.as_view(), name='create_tgo_object_resource'),

    path('edit/<int:pk>', TGOUpdateView.as_view(), name='edit'),
    path('edit_tgo_object/<int:pk>', TGO_objectUpdateView.as_view(), name='edit_tgo_object'),
    path('edit_resource/<int:pk>', ResourceUpdateView.as_view(), name='edit_resource'),

    path('delete/tgo_object/<int:pk>/', TGO_objectDeleteView.as_view(), name='delete_tgo_object'),
    path('delete/resource/<int:pk>/', ResourceDeleteView.as_view(), name='delete_resource'),    

    path('copy_tgo/<int:pk>', copy_tgo, name='copy_tgo'),
]

urlpatterns += [
    path('ajax_update_tgo', update_tgo, name='ajax_update_tgo'), 
]
