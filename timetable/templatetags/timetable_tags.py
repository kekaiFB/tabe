from django import template
register = template.Library()
from ..models import Timetable
from datetime import datetime


@register.simple_tag
def timetable_history_tag(timetable):
    list_timetable = []
    res = Timetable.history.select_related().order_by('-history_date')
    for elem in timetable:
        count = 0
        listField = []
       
        for r in res:
            if r.id == elem.id:
                if count == 0:
                    count+=1
                    listField.append(r.history_date)
                    new_record = r
                elif count == 1:
                    count+=1
                    old_record = r
                    delta = new_record.diff_against(old_record)
                    for change in delta.changes:
                        listField.append(change.field)
                    list_timetable.append(listField)
                elif count > 1:
                    
                    break
                else:
                    pass

        if len(listField) == 1:
            list_timetable.append([datetime.now()])
    return list_timetable 


@register.inclusion_tag('timetable/my_tags/classTimetable.html')
def classTimetable( t_value=0, t_label='', th = []):
    style = ''
    clas = []
    th_date = th[0]
    th_date = datetime(th_date.year, th_date.month, th_date.day, th_date.hour, th_date.minute, th_date.second,  th_date.microsecond)   
    difference_minutes = (datetime.now()-th_date).total_seconds() / (60*60)
    if t_label in th:
        if difference_minutes < 10:
            clas = ["fw-bold", "text-white"]
            style = "#f00"
        elif difference_minutes < 30:
            clas = ["fw-bold", "text-white"]
            style = "#ff4f4f"
        elif difference_minutes < 60: 
            style = "#fc7979"
        elif difference_minutes < 240: 
            style = "#ffa1a1"
        elif difference_minutes < 480: 
            style = "#ffd1d1"
        elif difference_minutes < 1440: 
            style = "#f1f2a7"
        elif difference_minutes < 2880: 
            style = "#feffcc"
        elif difference_minutes < 10080: 
            style = "#f9fae1"
    return { 't_value': t_value,  't_label': t_label, 'style': style, 'clas': clas}


@register.simple_tag
def background(timetablestatusight):
    timetablestatusight = str(timetablestatusight)
    style = ''
    if timetablestatusight == 'Действует':
        pass
    elif timetablestatusight == 'На согласовании':
        style = "#fbff0d"
    elif timetablestatusight == 'Тестирование':
        style = "#8cc8ff"
    elif timetablestatusight == 'Отменен':
        pass
    elif timetablestatusight == 'Отказано':
        pass
    elif timetablestatusight == 'Заявка':
        style = "#6da3d6"
    
    return style


@register.simple_tag
def color(timetablestatusight):
    timetablestatusight = str(timetablestatusight)
    color = ''
    if timetablestatusight == 'Действует':
        pass
    elif timetablestatusight == 'На согласовании':
        pass
    elif timetablestatusight == 'Тестирование':
        pass
    elif timetablestatusight == 'Отменен':
        color = 'grey'
    elif timetablestatusight == 'Отказано':
        color = 'red'
    elif timetablestatusight == 'Заявка':
        pass
    
    return color