
from django import template
from django.utils.translation import gettext_lazy

register = template.Library()


@register.filter('trans_s')
def trans_filter(text):
    return gettext_lazy(text)



@register.filter('sample')
def sample_filter(text):
    text = gettext_lazy('sample')
    return text