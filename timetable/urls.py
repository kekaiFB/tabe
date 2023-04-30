from django.urls import path
from .views import *

app_name = 'timetable'

urlpatterns = [
    path('', TimetableListView.as_view(), name='timetable_list'),
    path('add_timetable_list/', TimetableListCreateView.as_view(), name='add_timetable_list'),
    path('edit_timetable_list/<int:pk>', TimetableListUpdateView.as_view(), name='edit_timetable_list'),
    path('delete_timetable_list/<int:pk>/',TimetableListDeleteView.as_view(), name='delete_timetable_list'),
    path('copy_timetable/<int:pk>', copy_timetable, name='copy_timetable'),

    #-------------Расписание-----------------------------------------------------------------
    path("timetable/<str:title>/<int:id>/", TimeTableView.as_view(), name='index'),
    path('add_timetable/<int:timetable_id>/', TimeTableCreateView.as_view(), name='add_timetable'),
    path('edit_timetable/<int:pk>', TimeTableUpdateView.as_view(), name='edit_timetable'),
    path('delete_timetable/<int:pk>/', TimeTableDeleteView.as_view(), name='delete_timetable'),

    path("timetable_week/<str:title>/<int:id>", TimeTableWeekView.as_view(), name='index_week'),
    path('add_timetable_week/<int:timetable_id>/', TimeTableWeekCreateView.as_view(), name='add_timetable_week'),
    path('edit_timetable_week/<int:pk>', TimeTableWeekUpdateView.as_view(), name='edit_timetable_week'),
    path('delete_timetable_week/<int:pk>/', TimeTableWeekDeleteView.as_view(), name='delete_timetable_week'),

    path("timetable_week_group/<str:title>/<int:id>/", TimeTableWeekGroupView.as_view(), name='index_week_group'),
    path('add_timetable_week_group/<int:timetable_id>/', TimeTableWeekGroupCreateView.as_view(), name='add_timetable_week_group'),
    path('edit_timetable_week_group/<int:pk>', TimeTableWeekGroupUpdateView.as_view(), name='edit_timetable_week_group'),
    path('delete_timetable_week_group/<int:pk>/', TimeTableWeekGroupDeleteView.as_view(), name='delete_timetable_week_group'),
    #-------------Расписание конец-----------------------------------------------------------------

    
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

    path('type_flight/', TypeFlightView.as_view(), name='type_flight'),
    path('add_type_flight/', TypeFlightCreateView.as_view(), name='add_type_flight'),
    path('edit_type_flight/<int:pk>', TypeFlightUpdateView.as_view(), name='edit_type_flight'),
    path('delete_type_flight/<int:pk>/', TypeFlightDeleteView.as_view(), name='delete_type_flight'),

    path('type_country/', TypeCountryView.as_view(), name='type_country'),
    path('add_type_country/', TypeCountryCreateView.as_view(), name='add_type_country'),
    path('edit_type_country/<int:pk>', TypeCountryUpdateView.as_view(), name='edit_type_country'),
    path('delete_type_country/<int:pk>/', TypeCountryDeleteView.as_view(), name='delete_type_country'),

    path('equipmentAirplane/', EquipmentAirplaneView.as_view(), name='equipmentAirplane'),
    path('add_equipmentAirplane/', EquipmentAirplaneCreateView.as_view(), name='add_equipmentAirplane'),
    path('edit_equipmentAirplane/<int:pk>', EquipmentAirplaneUpdateView.as_view(), name='edit_equipmentAirplane'),
    path('delete_equipmentAirplane/<int:pk>/', EquipmentAirplaneDeleteView.as_view(), name='delete_equipmentAirplane'),

    path('timetableStatus/', TimetableStatusView.as_view(), name='timetableStatus'),
    path('add_timetableStatus/', TimetableStatusCreateView.as_view(), name='add_timetableStatus'),
    path('edit_timetableStatus/<int:pk>', TimetableStatusUpdateView.as_view(), name='edit_timetableStatus'),
    path('delete_timetableStatus/<int:pk>/', TimetableStatusDeleteView.as_view(), name='delete_timetableStatus'),

    path('historyTimetable/<int:id>', HistoryTimetableView.as_view(), name='historyTimetable'),
    path('editHistoryObject/<int:pk>/<int:history_id>/', editHistoryObject, name='editHistoryObject'),
    path('delete_historyTimetable/<int:pk>/<int:history_id>/', HistoryTimetableDeleteView.as_view(), name='delete_historyTimetable'),
]


urlpatterns += [
    path('ajax_load_flight', load_ajax_fligh_data, name='ajax_load_flight'), 
]