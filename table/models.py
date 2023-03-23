from django.db import models
from datetime import timedelta

#Для post_save
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.db import models
from datetime import timedelta

#Для post_save
from django.dispatch import receiver
from django.db.models.signals import post_save


from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey  


class Office(models.Model):  
    title = models.CharField(max_length=150, db_index=True, verbose_name="Служба")  

    class Meta:
        verbose_name = 'Служба'
        verbose_name_plural = '1 Служба'

    def __str__(self):
        return self.title
            

class Post(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name="Служба")  
    title = models.CharField(max_length=150, db_index=True, verbose_name="Должность")

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = '2 Должности'

    def __str__(self):
        return self.title


class Human(models.Model):  
    office = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name="Служба")  
    post = ChainedForeignKey(
        Post, # the model where you're populating your countries from
        chained_field="office", # the field on your own model that this field links to 
        chained_model_field="office", # the field on Country that corresponds to newcontinent
        show_all=False, # only shows the countries that correspond to the selected continent in newcontinent
        verbose_name="Должность"
    )  
    initials = models.CharField(max_length=150, db_index=True, verbose_name="ФИО")  

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = '3 Люди'
   
    def __str__(self):
        return self.initials


class Reason(models.Model):  
    digital_code = models.CharField(max_length=10, verbose_name="Цифровой код") 
    character_code = models.CharField(max_length=10, verbose_name="Сивольный код") 
    title = models.CharField(max_length=150, verbose_name="Расшифровка") 

    class Meta:
        verbose_name = 'Причина пропуска'
        verbose_name_plural = '5 Причины пропуска' 

    def __str__(self):
        return self.title


class Shift(models.Model):  
    title = models.CharField(max_length=150, verbose_name="Название") 
    description = models.CharField(max_length=500, verbose_name="Описание")

    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = '6 Смены' 

    def __str__(self):
        return self.title
    

class ScheduleNotJob(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, verbose_name="Смена") 
    office = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name="Служба") 
    post = GroupedForeignKey(Post, "office") 
    human = GroupedForeignKey(Human, "post") 
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE, verbose_name="Причина")
    comment = models.CharField(max_length=300, blank=True, null=True, verbose_name="Примечание")
    length_time = models.IntegerField(blank=True, null=True, verbose_name="Длительность")
    date_start = models.DateField(blank=True, null=True, verbose_name="Начало") 
    date_end = models.DateField(blank=True, null=True, verbose_name="Окончание") 
    
    class Meta:
        verbose_name = 'Данные пропуска'
        verbose_name_plural = '7 Данные пропусков'

    def __str__(self):
        return str(self.human)

@receiver(post_save, sender=ScheduleNotJob)
def update_date_snj(sender, instance, **kwargs):
    if instance.length_time:
        date_end = instance.date_start + timedelta(days=instance.length_time - 1)
        sender.objects.filter(pk=instance.id).update(date_end=date_end.strftime('%Y-%m-%d'))
    elif instance.date_end:
        length_time = (instance.date_end - instance.date_start).days
        sender.objects.filter(pk=instance.id).update(length_time=length_time + 1)    
    else:
         sender.objects.filter(pk=instance.id).update(date_end=None)
