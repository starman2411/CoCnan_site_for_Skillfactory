from django import template
from board.models import Post, Response

register = template.Library()


@register.simple_tag
def get_responses_amount(post):
    responses = Response.objects.filter(post = post)
    return len(responses)

