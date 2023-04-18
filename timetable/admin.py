# from django.contrib import admin
# from .models import (Airlines
#                      , Airplane
#                      , EquipmentAirplane
#                      )


# class AirlinesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'character_code',)
#     list_display_links = ('id', 'title', 'character_code',)
#     search_fields = ('id', 'title', 'character_code',)
    
# class AirplaneAdmin(admin.ModelAdmin):
#     list_display = ('id', 'airline', 'title',)
#     list_display_links = ('id', 'title',)
#     search_fields = ('id', 'airline', 'title',)

# class EquipmentAirplaneAdmin(admin.ModelAdmin):
#     list_display = ('id', 'airplane', 'equipment', 'seats',)
#     list_display_links =('id',)
#     search_fields = ('id', 'airplane', 'equipment', 'seats',)
    

# admin.site.register(Airlines, AirlinesAdmin)
# admin.site.register(Airplane, AirplaneAdmin)
# admin.site.register(EquipmentAirplane, EquipmentAirplaneAdmin)