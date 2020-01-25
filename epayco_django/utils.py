import hashlib

import pyepayco.epayco as Epayco
import requests
from django.conf import settings
from django.urls import reverse

from .settings import epayco_settings


def get_signature(cust_id_client, p_key, ref_payco, transaction_id, amount, currency_code):
    """
        Genera el signature requerido por ePayco para verificar una confirmación.
    """
    signature = '{}^{}^{}^{}^{}^{}'.format(cust_id_client, p_key, ref_payco,
                                           transaction_id, amount, currency_code)
    return hashlib.sha256(signature.encode('utf')).hexdigest()


def validate_response_code(ref_payco, request=None):
    from .models import PaymentConfirmation
    options = {'apiKey': epayco_settings.PUBLIC_KEY,
               'privateKey': epayco_settings.PRIVATE_KEY,
               'test': epayco_settings.TEST,
               'lenguage': 'ES'}
    epayco = Epayco.Epayco(options)
    qs = PaymentConfirmation.objects.filter(ref_payco__iexact=ref_payco)

    if not qs.exists():
        response = epayco.cash.get(ref_payco)  # Validate the reference
        if response['success'] == True:
            result = requests.post(settings.BASE_URL + reverse('epayco_confirmation'), data=response['data'])
            flag = result.json()['flag']
            obj = PaymentConfirmation.objects.filter(ref_payco__iexact=ref_payco).last()
            return {'valid_ref': True, 'existed': False, 'flag': flag, 'obj': obj}
        return {'valid_ref': False}
    elif qs.filter(flag=False).exists():
        obj = qs.first()
        return {'valid_ref': True, 'existed': True, 'flag': False, 'obj': obj}
    else:
        obj = qs.first()
        return {'valid_ref': True, 'existed': True, 'flag': True, 'obj': obj}
