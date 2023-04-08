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
def button_add_resource(clas, url='', id=0, tgo_id=0):
    return {'clas': clas, 'url': url, 'id': str(id), 'tgo_id': str(tgo_id)}


@register.inclusion_tag('table_tgo/my_tags/button_add.html')
def button_add(clas, url='', id=0):
    return {'clas': clas, 'url': url, 'id': str(id)}


@register.inclusion_tag('table_tgo/my_tags/button_add_operation.html')
def button_add_operation(clas, url='', id=0):
    return {'clas': clas, 'url': url, 'id': str(id)}


@register.inclusion_tag('table_tgo/my_tags/del_button.html')
def del_button(clas, url='', id=0):
    return {'clas': clas, 'url': url, 'id': str(id)}


@register.inclusion_tag('table_tgo/my_tags/button_edit.html')
def edit_button(clas, url='', id=0):
    return {'clas': clas, 'url': url, 'id': str(id)}
