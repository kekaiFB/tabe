from django import template
register = template.Library()


@register.simple_tag
def unique_list(lsit):
    unique_list = set()
    for elem in lsit:
        unique_list.add(elem.ressource.office.title)
    objects = ' '.join(unique_list)
    return str(objects)


@register.inclusion_tag('table_tgo/my_tags/button_add_resource.html')
def button_add_resource(url='', id=0, tgo_id=0):
    return {'url': url, 'id': str(id), 'tgo_id': str(tgo_id)}


@register.inclusion_tag('table_tgo/my_tags/button_add.html')
def button_add(url='', id=0):
    return {'url': url, 'id': str(id)}


@register.inclusion_tag('table_tgo/my_tags/button_add_operation.html')
def button_add_operation(url='', id=0):
    return {'url': url, 'id': str(id)}


@register.inclusion_tag('table_tgo/my_tags/del_button.html')
def del_button(url='', id=0):
    return {'url': url, 'id': str(id)}


@register.inclusion_tag('table_tgo/my_tags/button_edit.html')
def edit_button(url='', id=0):
    return {'url': url, 'id': str(id)}


@register.inclusion_tag('table_tgo/my_tags/del_button_text.html')
def button_text(clas, url='', id=0, text=''):
    return {'clas': clas, 'url': url, 'id': str(id), 'text': text}


@register.inclusion_tag('table_tgo/my_tags/copy_button.html')
def copy_button(url='', id=0, title='', ModalTitle=''):
    return {'url': url, 'id': str(id), 'title': title, 'ModalTitle': ModalTitle}



@register.inclusion_tag('table_tgo/my_tags/add_button_text.html')
def add_button_text(url=''):
    return {'url': url}





#--------------РАСПИСАНИЕ------------


@register.inclusion_tag('timetable/my_tags/del_button.html')
def del_button_timetable(url='', id=0, history_id = 0):
    return {'url': url, 'id': str(id), 'history_id': str(history_id)}