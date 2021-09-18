from django import template

from ..settings import epayco_settings

register = template.Library()


@register.inclusion_tag("epayco_web_checkout_button.html")
def render_checkout(
    amount,
    name,
    tax=0,
    tax_base=0,
    description="",
    currency="COP",
    country_code="co",
    external=True,
    extra1="",
    extra2="",
    extra3="",
    extra4="",
    extra5="",
    extra6="",
    extra7="",
    extra8="",
    extra9="",
    extra10="",
    same_site=True,
    request=None,
    response_url=None,
    **kwargs
):
    if description == "":
        description = name

    if epayco_settings.CONFIRMATION_URL.startswith("http"):
        confirmation_url = epayco_settings.CONFIRMATION_URL
    else:
        confirmation_url = request.build_absolute_uri(epayco_settings.CONFIRMATION_URL)

    if epayco_settings.FORCE_HTTPS and "https://" not in confirmation_url:
        confirmation_url = confirmation_url.replace("http://", "https://")

    if not response_url:
        if epayco_settings.CONFIRMATION_URL.startswith("http"):
            response_url = epayco_settings.RESPONSE_URL
        else:
            response_url = request.build_absolute_uri(epayco_settings.RESPONSE_URL)

    if epayco_settings.FORCE_HTTPS and "https://" not in response_url:
        response_url = response_url.replace("http://", "https://")

    return {
        "public_key": epayco_settings.PUBLIC_KEY,
        "amount": amount,
        "tax": tax,
        "tax_base": tax_base,
        "name": name,
        "description": description,
        "currency": currency,
        "country_code": country_code,
        "test": "{}".format(epayco_settings.TEST).lower(),
        "external": "{}".format(external).lower(),
        "extra1": extra1,
        "extra2": extra2,
        "extra3": extra3,
        "extra4": extra4,
        "extra5": extra5,
        "extra6": extra6,
        "extra7": extra7,
        "extra8": extra8,
        "extra9": extra9,
        "extra10": extra10,
        "response_url": response_url,
        "confirmation_url": confirmation_url,
        "same_site": same_site,
    }
