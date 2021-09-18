import hashlib

import epaycosdk.epayco as Epayco
import requests

from .settings import epayco_settings


def get_signature(cust_id_client, p_key, ref_payco, transaction_id, amount, currency_code):
    """
    Genera el signature requerido por ePayco para verificar una confirmación.
    """
    signature = "{}^{}^{}^{}^{}^{}".format(cust_id_client, p_key, ref_payco, transaction_id, amount, currency_code)
    return hashlib.sha256(signature.encode("utf")).hexdigest()


def validate_response_code(ref_payco, request=None):
    """
    Verifica el ref_payco. Funciona con los 2 tipos de ref_payco.

    :param ref_payco:
    :param request:
    :return:
    """

    if not ref_payco:
        return {"valid_ref": False}

    from .models import PaymentConfirmation

    options = {
        "apiKey": epayco_settings.PUBLIC_KEY,
        "privateKey": epayco_settings.PRIVATE_KEY,
        "test": epayco_settings.TEST,
        "lenguage": "ES",
    }

    response = None
    if not ref_payco.isdigit():
        response = requests.get("https://secure.epayco.co/validation/v1/reference/{}".format(ref_payco))
        try:
            response = response.json()
        except:
            return {"valid_ref": False}
        ref_payco = str(response["data"]["x_ref_payco"])

    qs = PaymentConfirmation.objects.filter(ref_payco__iexact=ref_payco).exclude(cod_transaction_state=3)
    if not qs.exists():
        if not response:
            epayco = Epayco.Epayco(options)
            response = epayco.cash.get(ref_payco)

        # Validate the reference
        if response["success"] == True:
            if epayco_settings.CONFIRMATION_URL.startswith("http"):
                url = epayco_settings.CONFIRMATION_URL
            else:
                url = "{}://{}{}".format(
                    "https" if epayco_settings.FORCE_HTTPS or request.is_secure() else "http",
                    request.get_host(),
                    epayco_settings.CONFIRMATION_URL,
                )
            r2 = requests.post(url, data=response["data"])
            if r2.status_code == 405:
                raise Exception(
                    "There seems the be an error reaching the confirmation URL."
                    ' Please make sure you are making good use of the "FORCE_HTTPS" setting.'
                )
            obj = PaymentConfirmation.objects.filter(ref_payco__iexact=ref_payco).last()
            if obj:
                return {"valid_ref": True, "existed": False, "flag": obj.is_flagged, "obj": obj}
            else:
                return {""}
        return {"valid_ref": False}
    elif qs.filter(flag=False).exists():
        obj = qs.filter(flag=False).last()
        return {"valid_ref": True, "existed": True, "flag": False, "obj": obj}
    else:
        obj = qs.last()
        return {"valid_ref": True, "existed": True, "flag": True, "obj": obj}


def get_valid_keys():
    return [
        "cust_id_cliente",
        "ref_payco",
        "id_invoice",
        "description",
        "amount",
        "amount_country",
        "amount_ok",
        "tax",
        "amount_base",
        "currency_code",
        "bank_name",
        "cardnumber",
        "quotas",
        "response",
        "approval_code",
        "transaction_id",
        "transaction_date",
        "cod_response",
        "response_reason_text",
        "errorcode",
        "cod_transaction_state",
        "transaction_state",
        "franchise",
        "business",
        "customer_doctype",
        "customer_document",
        "customer_name",
        "customer_lastname",
        "customer_email",
        "customer_phone",
        "customer_movil",
        "customer_ind_pais",
        "customer_country",
        "customer_city",
        "customer_address",
        "customer_ip",
        "signature",
        "test_request",
        "extra1",
        "extra2",
        "extra3",
        "extra4",
        "extra5",
        "extra6",
        "extra7",
        "extra8",
        "extra9",
        "extra10",
    ]
