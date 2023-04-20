from django.contrib import admin
from .models import (Airlines
                     , Airplane
                     , EquipmentAirplane
                     , TypeCountry
                     , Country
                     , City
                     , Airport
                     , TypeFlight
                     , Flight
                     , Ttimetable
                     , TtimetableStatus
                     )


# ----------------------АВИАКОМПАНИИ---------------------------------------------------------

class AirlinesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'character_code',)
    list_display_links = ('id', 'title', 'character_code',)
    search_fields = ('id', 'title', 'character_code',)
    
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('id', 'airline', 'title',)
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'airline', 'title',)

class EquipmentAirplaneAdmin(admin.ModelAdmin):
    list_display = ('id', 'airplane', 'equipment', 'seats',)
    list_display_links =('id',)
    search_fields = ('id', 'airplane', 'equipment', 'seats',)
    

admin.site.register(Airlines, AirlinesAdmin)
admin.site.register(Airplane, AirplaneAdmin)
admin.site.register(EquipmentAirplane, EquipmentAirplaneAdmin)

# -------------------------------------------------------------------------------
# 
#    
# -------------------------ЛОКАЦИИ------------------------------------------------------
class TypeCountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links =  ('id', 'title',)
    search_fields = ('id', 'title',)
    
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type')
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title', 'type')

admin.site.register(TypeCountry, TypeCountryAdmin)
admin.site.register(Country, CountryAdmin)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country', 'get_type',)
    list_display_links =('id', 'title')
    search_fields = ('id', 'title', 'country', 'get_type',)

    def get_queryset(self, request):
        return super(CityAdmin,self).get_queryset(request).select_related()

    @admin.display(ordering='country', description='Тип страны')
    def get_type(self, obj):
        return obj.country.type


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'city', 'get_country',)
    list_display_links =('id', 'title')
    search_fields = ('id', 'title', 'city', 'get_country',)

    def get_queryset(self, request):
        return super(AirportAdmin,self).get_queryset(request).select_related()

    @admin.display(ordering='country', description='Страна')
    def get_country(self, obj):
        return obj.city.country


# -------------------------------------------------------------------------------
# 
# 
# -------------------------РЕЙСЫ------------------------------------------------------
@admin.register(TypeFlight)
class TypeFlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links =('id', 'title',)
    search_fields = ('id', 'title',)

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'airline', 'airplane', 'equipmentseats', 'arrival',  'departure', 'departurelAirport', 'arrivalAirport')
    list_display_links =('id', 'title',)
    search_fields = ('id', 'title', 'type', 'airline', 'airplane', 'equipmentseats',  'arrival',  'departure', 'departurelAirport', 'arrivalAirport')

    def get_queryset(self, request):
        return super(FlightAdmin,self).get_queryset(request).select_related()

    @admin.display(ordering='airplane', description='Количество мест')
    def equipmentseats(self, obj):
        return obj.equipmentAirplane.seats
    
    # @admin.display(ordering='airplane', description='Тип страны')
    # def typeCountry(self, obj):
    #     return obj.arrival.country.type

admin.site.register(Ttimetable)
admin.site.register(TtimetableStatus)
