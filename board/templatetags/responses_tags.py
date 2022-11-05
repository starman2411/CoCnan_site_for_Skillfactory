from django import template
from django.db.models.query import QuerySet
import json

register = template.Library()


@register.simple_tag
def get_responses_texts(arr):
    responses_dict = {}
    if type(arr) == QuerySet:
        responses_dict.update([(elem.pk, str(elem.text)) for elem in arr])
        return json.dumps(responses_dict)
    return json.dumps(responses_dict)
