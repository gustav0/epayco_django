import hashlib

import epaycosdk.epayco as Epayco
import requests

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
    qs = PaymentConfirmation.objects.filter(ref_payco__iexact=ref_payco)
    if not qs.exists():
        epayco = Epayco.Epayco(options)
        response = epayco.cash.get(ref_payco)  # Validate the reference
        if response['success'] == True:
            if epayco_settings.CONFIRMATION_URL.startswith('http'):
                url = epayco_settings.CONFIRMATION_URL
            else:
                url = '{}://{}{}'.format('https' if epayco_settings.FORCE_HTTPS or request.is_secure() else 'http',
                                         request.get_host(), epayco_settings.CONFIRMATION_URL)
            r2 = requests.post(url, data=response['data'])
            if r2.status_code == 405:
                raise Exception('There seems the be an error reaching the confirmation URL.'
                                ' Please make sure you are making good use of the "FORCE_HTTPS" setting.')
            obj = PaymentConfirmation.objects.filter(ref_payco__iexact=ref_payco).last()
            if obj:
                return {'valid_ref': True, 'existed': False, 'flag': obj.is_flagged, 'obj': obj}
            else:
                return {''}
        return {'valid_ref': False}
    elif qs.filter(flag=False).exists():
        obj = qs.filter(flag=False).first()
        return {'valid_ref': True, 'existed': True, 'flag': False, 'obj': obj}
    else:
        obj = qs.first()
        return {'valid_ref': True, 'existed': True, 'flag': True, 'obj': obj}
