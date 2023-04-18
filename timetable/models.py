# from django.db import models
# from datetime import timedelta

# #Для post_save
# from django.dispatch import receiver
# from django.db.models.signals import post_delete, post_save
# from django.core.cache import cache 

# from smart_selects.db_fields import ChainedForeignKey


# class Airlines(models.Model):  
#     title = models.CharField(max_length=150, verbose_name="Название")
#     character_code = models.CharField(max_length=10, verbose_name="Код", default='', blank=True) 

#     class Meta:
#         verbose_name = 'Авиакомпания'
#         verbose_name_plural = '1 Авиакомпании' 

#     def __str__(self):
#         return self.title
    


# class Airplane(models.Model):
#     airline = models.ForeignKey(Airlines, on_delete=models.CASCADE, verbose_name="Авиакомпания")
#     title = models.CharField(max_length=150, verbose_name="Название")
    
#     class Meta:
#         verbose_name = 'Воздушное судно'
#         verbose_name_plural = '2 ВС' 

#     def __str__(self):
#         return self.title
    

# class EquipmentAirplane(models.Model):
#     airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, verbose_name="ВС")
#     equipment = models.CharField(max_length=50, verbose_name="Комплектация") 
#     seats = models.IntegerField(blank=True, null=True, verbose_name="Количество мест")

#     class Meta:
#         verbose_name = 'Комплектация воздушного судна'
#         verbose_name_plural = '3 Комплектация ВС' 

#     def __str__(self):
#         return self.equipment
    
  
# # Воздушные суда (ВС) под Авиакоманию
# # комплектация под каждое ВС 

# # Тип страны
# # Страны

# # Города под Страну

# # Тип рейса
# # Рейсы

# # Статус расписания
# # Расписание
# # под каждую запись (Расписание должен быть пользователь который создал, и который изменил)
