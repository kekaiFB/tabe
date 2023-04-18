from django.db import models
from datetime import timedelta

#Для post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache 

from smart_selects.db_fields import ChainedForeignKey

# ----------------------АВИАКОМПАНИИ---------------------------------------------------------
class Airlines(models.Model):  
    title = models.CharField(max_length=150, verbose_name="Название")
    character_code = models.CharField(max_length=10, verbose_name="Код", default='', blank=True) 

    class Meta:
        verbose_name = 'Авиакомпания'
        verbose_name_plural = '1 Авиакомпании' 

    def __str__(self):
        return self.title
    

class Airplane(models.Model):
    airline = models.ForeignKey(Airlines, on_delete=models.CASCADE, verbose_name="Авиакомпания")
    title = models.CharField(max_length=150, verbose_name="Название")
    
    class Meta:
        verbose_name = 'Воздушное судно'
        verbose_name_plural = '2 ВС' 

    def __str__(self):
        return self.title
    

class EquipmentAirplane(models.Model):
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, verbose_name="ВС")
    equipment = models.CharField(max_length=50, verbose_name="Комплектация") 
    seats = models.IntegerField(blank=True, null=True, verbose_name="Количество мест")

    class Meta:
        verbose_name = 'Комплектация воздушного судна'
        verbose_name_plural = '3 Комплектация ВС' 

    def __str__(self):
        return self.equipment
# -------------------------------------------------------------------------------
# 
# 
#    
# -------------------------ЛОКАЦИИ------------------------------------------------------
class TypeCountry(models.Model):  
    title = models.CharField(max_length=150, verbose_name="Название")

    class Meta:
        verbose_name = 'Тип страны'
        verbose_name_plural = '4 Типы стран' 

    def __str__(self):
        return self.title
    

class Country(models.Model):  
    title = models.CharField(max_length=150, verbose_name="Название")
    type = models.ForeignKey(TypeCountry, on_delete=models.CASCADE, verbose_name="Тип")

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = '5 Страны' 

    def __str__(self):
        return self.title


class City(models.Model):  
    title = models.CharField(max_length=150, verbose_name="Название")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна")

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = '6 Города' 

    def __str__(self):
        return self.title
# -------------------------------------------------------------------------------
# 
# 
#    
# -------------------------РЕЙСЫ------------------------------------------------------
class TypeFlight(models.Model):  
    title = models.CharField(max_length=150, verbose_name="Название")

    class Meta:
        verbose_name = 'Тип рейса'
        verbose_name_plural = '7 Типы рейсов' 

    def __str__(self):
        return self.title
    

class Flight(models.Model):  
    title = models.CharField(max_length=150, verbose_name="№ рейса")
    type = models.ForeignKey(TypeFlight, on_delete=models.CASCADE, verbose_name="Тип")
    airline = models.ForeignKey(Airlines, on_delete=models.CASCADE, verbose_name="Аваиакомпания")
    # airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, verbose_name="Воздушное судно")
    airplane = ChainedForeignKey(
        Airplane,
        chained_field="airline",
        chained_model_field="airline",
        show_all=False, 
        verbose_name="Воздушное судно"
    )
    arrival = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Прилет", related_name="arrival")
    departure = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Вылет", related_name="departure")


    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = '8 Рейсы' 

    def __str__(self):
        return self.title
# -------------------------------------------------------------------------------
# 
# 
#    
# -------------------------РАСПИСАНИЕ------------------------------------------------------    

# Статус расписания
# Расписание
# под каждую запись (Расписание должен быть пользователь который создал, и который изменил)
