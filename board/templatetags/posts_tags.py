from django import template
from django.db.models.query import QuerySet

register = template.Library()


@register.simple_tag
def get_pks(arr):
    if type(arr) == QuerySet:
        pks_list = [elem.pk for elem in arr]
        return pks_list
    return None

