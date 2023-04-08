from django.db import models
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey
from table.models import Office

#Для post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache 


class Operation(models.Model):  
    title = models.CharField(max_length=150, db_index=True, verbose_name="Операция")  

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = '1 Операция'

    def __str__(self):
        return self.title
    

class Ressource(models.Model):  
    title = models.CharField(max_length=150, db_index=True, verbose_name="Ресурс")  
    office = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name="Служба") 

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = '2 Ресурс'

    def __str__(self):
        return self.title


class TGO(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="ТГО")  
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'ТГО'
        verbose_name_plural = '3 ТГО'
        ordering = ['id']


    def get_absolute_url(self):
       return reverse('table_tgo:tgo_objects', kwargs={'id': self.id, 'title': self.title})
    
    def __str__(self):
        return self.title
    

class TGO_object(models.Model):
    tgo = models.ForeignKey(TGO, on_delete=models.CASCADE, verbose_name="ТГО")  
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name="Операция")  
    ressource = models.ManyToManyField(Ressource, through='RessourceOperation') 
    order = models.PositiveIntegerField(verbose_name="Пункт")
    time_start = models.CharField(max_length=8, blank=True, null=True, default='0', verbose_name="Начало")
    time_lenght = models.CharField(max_length=8, blank=True, null=True, default='0', verbose_name="Длительность")
    time_end = models.CharField(max_length=8, blank=True, null=True, default='0', verbose_name="Конец")

    class Meta:
        verbose_name = 'Объект ТГО'
        verbose_name_plural = '4 Объект ТГО'
        ordering = ['order'] 

    def __str__(self):
        return self.operation.title
    

class RessourceOperation(models.Model):
    tgo = models.ForeignKey(TGO, on_delete=models.CASCADE, verbose_name="ТГО", related_name='res_operation')  
    tgo_object = ChainedForeignKey(
        TGO_object, # the model where you're populating your countries from
        chained_field="tgo", # the field on your own model that this field links to 
        chained_model_field="tgo", # the field on Country that corresponds to newcontinent
        show_all=False, # only shows the countries that correspond to the selected continent in newcontinent
        verbose_name="Объект ТГО"
        , related_name='res_operations'
    )
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE, verbose_name="Ресурс", related_name='res_operation')
    count = models.PositiveIntegerField( verbose_name="Количество")
    time_start = models.CharField(max_length=8, blank=True, null=True, default='0', verbose_name="Начало")
    time_lenght = models.CharField(max_length=8, blank=True, null=True, default='0', verbose_name="Длительность")
    time_end = models.CharField(max_length=8, blank=True, null=True, default='0', verbose_name="Конец")


    class Meta:
        verbose_name = 'Ресурс для операции в ТГО'
        verbose_name_plural = '5 Ресурсы для операции в ТГО'
        ordering = ['id']

    def __str__(self):
        return str(self.tgo_object.tgo.title) + ' ' + self.ressource.title