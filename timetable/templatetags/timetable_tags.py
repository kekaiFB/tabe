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
        style = "#bae8e8"
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


@register.simple_tag
def check_days_week(dw='', t=[]):
    if t.monday and dw == 'monday':
        return  1
    elif t.tuesday and dw == 'tuesday':
        return  2
    elif t.wednesday and dw == 'wednesday':
        return  3
    elif t.thursday and dw == 'thursday':
        return  4
    elif t.friday and dw == 'friday':
        return  5
    elif t.saturday and dw == 'saturday':
        return  6
    elif t.sunday and dw == 'sunday':
        return  7
    else:
        return None


@register.inclusion_tag('timetable/my_tags/checkedBolean.html')
def next_day_status(next_day_status=True):
    return {'next_day_status': next_day_status}


@register.inclusion_tag('timetable/my_tags/class_next_day_status.html')
def class_next_day_status(t_value=0, t_label='', th = []):
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
def label_week(dws=0):
    if dws == 1:
        return 'Понедельник'
    elif dws == 2:
        return 'Втроник'
    elif dws == 3:
        return 'Среда'
    elif dws == 4:
        return 'Четверг'
    elif dws == 5:
        return 'Пятница'
    elif dws == 6:
        return 'Суббота'
    elif dws == 7:
        return 'Воскресенье'
    else:
        pass