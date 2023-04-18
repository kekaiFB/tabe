from django.contrib import admin
from .models import (Airlines
                     , Airplane
                     , EquipmentAirplane
                     , TypeCountry
                     , Country
                     , City
                     , TypeFlight
                     , Flight
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

class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country')
    list_display_links =('id', 'title')
    search_fields = ('id', 'title', 'country')


admin.site.register(TypeCountry, TypeCountryAdmin)
admin.site.register(Country, CountryAdmin)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country', 'get_type',)
    list_display_links =('id', 'title')
    search_fields = ('id', 'title', 'country', 'get_type',)

    def get_queryset(self, request):
        return super(CityAdmin,self).get_queryset(request).select_related()

    @admin.display(ordering='country', description='Country')
    def get_type(self, obj):
        return obj.country.type



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
    list_display = ('id', 'title', 'type', 'airline', 'airplane',  'arrival',  'departure',)
    list_display_links =('id', 'title',)
    search_fields = ('id', 'title', 'type', 'airline', 'airplane',  'arrival',  'departure',)
