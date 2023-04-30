from django.db import models
from datetime import datetime, timedelta


from django.urls import reverse
from django.contrib.auth.models import User

from smart_selects.db_fields import ChainedForeignKey
from simple_history.models import HistoricalRecords
from table_tgo.models import TGO

#------------------АВИАКОМПАНИИ---------------------------------------------------------
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
        verbose_name_plural = '2.1 Комплектация ВС' 

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
        verbose_name_plural = '3 Типы стран' 

    def __str__(self):
        return self.title
    

class Country(models.Model):  
    title = models.CharField(max_length=150, verbose_name="Название")
    type = models.ForeignKey(TypeCountry, on_delete=models.CASCADE, verbose_name="Тип")

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = '3.1 Страны' 

    def __str__(self):
        return self.title


class City(models.Model):  
    title = models.CharField(max_length=150, verbose_name="Название")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна")

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = '3.2 Города' 

    def __str__(self):
        return self.title
    

class Airport(models.Model):  
    title = models.CharField(max_length=150, verbose_name="Название")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")

    class Meta:
        verbose_name = 'Аэропорт'
        verbose_name_plural = '3.3 Аэропорты' 

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
        verbose_name_plural = '4 Типы рейсов' 

    def __str__(self):
        return self.title
    

class Flight(models.Model):  
    title = models.CharField(max_length=150, verbose_name="№ рейса")
    type = models.ForeignKey(TypeFlight, on_delete=models.CASCADE, verbose_name="Тип")

    airline = models.ForeignKey(Airlines, on_delete=models.CASCADE, verbose_name="Аваиакомпания")
    #airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, verbose_name="Воздушное судно")
    airplane = ChainedForeignKey(
        Airplane, 
        chained_field="airline", 
        chained_model_field="airline",
        verbose_name="Воздушное судно"
    )
    equipmentAirplane = ChainedForeignKey(
        EquipmentAirplane, 
        chained_field="airplane", 
        chained_model_field="airplane",
        verbose_name="Комплектация"
    )
    #equipmentAirplane = models.ForeignKey(EquipmentAirplane, on_delete=models.CASCADE, verbose_name="Комплектация")
    
    departure = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Вылет", related_name="departure")
    arrival = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Прилет", related_name="arrival")
    type_flight =  models.CharField(max_length=150, verbose_name="Тип рейса")
    departurelAirport = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name="Аэропорт вылета", related_name="departurelAirport")
    arrivalAirport = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name="Аэропорт прилета", related_name="arrivalAirport")

    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = '4.1 Рейсы' 

    def __str__(self):
        return self.title 
    
    def get_path_flight(self):
        return str(self.departure) + ' - ' + str(self.arrival) 
# -------------------------------------------------------------------------------
# 
# 
#    
# -------------------------РАСПИСАНИЕ------------------------------------------------------    
class TimetableStatus(models.Model):  
    title = models.CharField(max_length=150, verbose_name="Название")

    class Meta:
        verbose_name = 'Статус расписания'
        verbose_name_plural = '5 Статусы расписания' 

    def __str__(self):
        return self.title
    

class TimetableList(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, db_index=True, verbose_name="Название")  
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Плановое расписание'
        verbose_name_plural = '5.1 Плановые расписания'
        ordering = ['id']


    def get_absolute_url(self):
       return reverse('timetable:index', kwargs={'id': self.id, 'title': self.title})
    
    def __str__(self):
        return self.title
    


class Timetable(models.Model):  
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="editor")
    timetablelist = models.ForeignKey(TimetableList, on_delete=models.CASCADE, verbose_name="Плановое расписание")  

    airline = models.ForeignKey(Airlines, on_delete=models.CASCADE, verbose_name="Аваиакомпания")
    #flight = models.ForeignKey(Flight, on_delete=models.CASCADE, verbose_name="Рейс")
    flight = ChainedForeignKey(
        Flight, 
        chained_field="airline", 
        chained_model_field="airline",
        verbose_name="Рейс"
    )
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False,  verbose_name="Прилет")
    departure_time = models.TimeField(auto_now=False, auto_now_add=False,  verbose_name="Вылет")
    next_day_status = models.BooleanField(default=False, verbose_name='Следующий день')

    start_register_time = models.TimeField(auto_now=False, auto_now_add=False,  verbose_name="Начало Регистрации")
    end_register_time = models.TimeField(auto_now=False, auto_now_add=False,  verbose_name="Конец Регистрации")

    date_start = models.DateField(blank=True, null=True, verbose_name="Начало действия") 
    date_end = models.DateField(blank=True, null=True, verbose_name="Конец действия") 
    
    tgo = models.ForeignKey(TGO, on_delete=models.CASCADE, verbose_name="ТГО")  

    timetablestatusight = models.ForeignKey(TimetableStatus, on_delete=models.CASCADE, verbose_name="Статус")
    comment = models.CharField(max_length=300, blank=True, null=True, default='', verbose_name="Комментарий")

    monday  = models.BooleanField(default=False, verbose_name='Понедельник')
    tuesday   = models.BooleanField(default=False, verbose_name='Вторник')
    wednesday   = models.BooleanField(default=False, verbose_name='Среда')
    thursday   = models.BooleanField(default=False, verbose_name='Четверг')
    friday   = models.BooleanField(default=False, verbose_name='Пятнциа')
    saturday   = models.BooleanField(default=False, verbose_name='Суббота')
    sunday   = models.BooleanField(default=False, verbose_name='Воскресенье')

    history = HistoricalRecords(verbose_name='Версия', cascade_delete_history=True, related_name='TimetableHistory')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = '5.2 Расписание' 

    def __str__(self):
        return str(self.flight)
    
    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret
    
    def date_lenght(self):
        return (self.date_end - self.date_start).days
    
    def parking(self):
       
        dt = str(self.departure_time.strftime('%H:%M'))
        at = str(self.arrival_time.strftime('%H:%M'))
        dt = datetime.strptime(dt, "%H:%M")  
        at = datetime.strptime(at, "%H:%M")
       
        if self.next_day_status:
            res = (timedelta(days=1) + dt) -at 
            if len(str(res)) == 14:
                seconds = res.total_seconds()
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                if len(str(minutes)) > 3:
                    return str(hours)[:2] + ':' + str(minutes)[:-2]
                else:
                    return str(hours)[:2] + ':0' + str(minutes)[:-2]
            else:
                return str(res)[:-3]
        else:
            return str(dt - at)[:-3]
        
            