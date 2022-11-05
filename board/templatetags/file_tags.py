from django import template

register = template.Library()


@register.simple_tag
def is_this_video(file_name):
    extension = file_name.split('.')[1]
    if extension == 'mp4':
        return True
    return False


@register.simple_tag
def is_this_img(file_name):
    extension = file_name.split('.')[1]
    if extension in ['gif', 'jpeg', 'png', 'jpg', 'svg']:
        return True
    return False


@register.simple_tag
def get_false():
    return False
