import json

import pyepayco.epayco as Epayco
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .models import PaymentConfirmation
from .settings import epayco_settings
from .utils import validate_response_code


@method_decorator(csrf_exempt, 'dispatch')
class ConfirmationView(View):

    def post(self, request, *args, **kwargs):
        data = {}
        for k, v in request.POST.items():
            if k in ('x_id_factura', 'x_respuesta',
                     'x_fecha_transaccion', 'x_cod_respuesta'):
                # Ignore fields in both English and Spanish
                continue
            data[k.replace('x_', '')] = v
        # TODO: Validate name consistency across all abstract models to prevent things like: id_user and customer_id.

        # Invert invoice name to keep the names consistent
        data['invoice_id'] = data['id_invoice']
        del data['id_invoice']

        # Get boolean fron the test_request attribute
        data['test_request'] = data['test_request'] == 'TRUE'
        data['raw'] = json.dumps(request.POST)

        # The AbstractFlagSegment's model's save method does the flagging validations.
        item = PaymentConfirmation.objects.create(**data)
        return JsonResponse({'flag': item.is_flagged}, status=200)


@method_decorator(csrf_exempt, 'dispatch')
class ResponseValidationView(View):

    def post(self, request, **kwargs):
        options = {'apiKey': epayco_settings.PUBLIC_KEY,
                   'privateKey': epayco_settings.PRIVATE_KEY,
                   'test': epayco_settings.TEST,
                   'language': 'ES'}
        epayco = Epayco(options)
        ref = request.POST.get('ref', None)
        if ref is None:
            return JsonResponse({'ref': ['This field is required.']}, status=400)

        validation = validate_response_code(ref)
        return JsonResponse(validation)
