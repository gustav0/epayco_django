from django import template
from django.conf import settings
from django.contrib.sites.models import Site

from ..settings import epayco_settings

register = template.Library()


@register.inclusion_tag('epayco_web_checkout_button.html')
def render_checkout(amount, name, tax=0, tax_base=0, description='', currency='COP', country_code='co',
                    external=True, extra1='', extra2='', extra3='', extra4='', extra5='', extra6='', extra7='',
                    extra8='', extra9='', extra10='', same_site=True, **kwargs):
    if same_site:
        domain = Site.objects.get(pk=settings.SITE_ID).domain
    else:
        domain = ''
    return {
        'public_key': epayco_settings.PUBLIC_KEY,
        'amount': amount, 'tax': tax, 'tax_base': tax_base,
        'name': name, 'description': description,
        'currency': currency, 'country_code': country_code,
        'test': epayco_settings.TEST, 'external': external,
        'extra1': extra1, 'extra2': extra2, 'extra3': extra3, 'extra4': extra4,
        'extra5': extra5, 'extra6': extra6, 'extra7': extra7, 'extra8': extra8,
        'extra9': extra9, 'extra10': extra10,
        'response_url': epayco_settings.RESPONSE_URL, 'confirmation_url': epayco_settings.CONFIRMATION_URL,

        'same_site': same_site,
        'domain': domain
    }
