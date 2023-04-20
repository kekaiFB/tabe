from django.urls import path
from .views import *

app_name = 'timetable'

urlpatterns = [
    path('', TimeTableView.as_view(), name='index'),
    path('add_timetable/', TimeTableCreateView.as_view(), name='add_timetable'),
    path('edit_timetable/<int:pk>', TimeTableUpdateView.as_view(), name='edit_timetable'),
    path('delete_timetable/<int:pk>/', TimeTableDeleteView.as_view(), name='delete_timetable'),
    
    path('airlines/', AirlinesView.as_view(), name='airlines'),
    path('add_airlines/', AirlinesCreateView.as_view(), name='add_airlines'),
    path('edit_airlines/<int:pk>', AirlinesUpdateView.as_view(), name='edit_airlines'),
    path('delete_airlines/<int:pk>/', AirlinesDeleteView.as_view(), name='delete_airlines'),
    
    path('airplane/', AirplaneView.as_view(), name='airplane'),
    path('add_airplane/', AirplaneCreateView.as_view(), name='add_airplane'),
    path('edit_airplane/<int:pk>', AirplaneUpdateView.as_view(), name='edit_airplane'),
    path('delete_airplane/<int:pk>/', AirplaneDeleteView.as_view(), name='delete_airplane'),
    
    path('country/', CountryView.as_view(), name='country'),
    path('add_country/',CountryCreateView.as_view(), name='add_country'),
    path('edit_country/<int:pk>', CountryUpdateView.as_view(), name='edit_country'),
    path('delete_country/<int:pk>/', CountryDeleteView.as_view(), name='delete_country'),
    
    path('city/', CityView.as_view(), name='city'),
    path('add_city/', CityCreateView.as_view(), name='add_city'),
    path('edit_city/<int:pk>', CityUpdateView.as_view(), name='edit_city'),
    path('delete_city/<int:pk>/', CityDeleteView.as_view(), name='delete_city'),
    
    path('airport/', AirportView.as_view(), name='airport'),
    path('add_airport/', AirportCreateView.as_view(), name='add_airport'),
    path('edit_airport/<int:pk>', AirportUpdateView.as_view(), name='edit_airport'),
    path('delete_airport/<int:pk>/', AirportDeleteView.as_view(), name='delete_airport'),
    
    path('flight/', FlightView.as_view(), name='flight'),
    path('add_flight/', FlightCreateView.as_view(), name='add_flight'),
    path('edit_flight/<int:pk>', FlightUpdateView.as_view(), name='edit_flight'),
    path('delete_flight/<int:pk>/', FlightDeleteView.as_view(), name='delete_flight'),


]

# urlpatterns += [
#     path('ajax_update_tgo', update_tgo, name='ajax_update_tgo'), 
# ]
