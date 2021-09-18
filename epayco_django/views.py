import json

from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView

from .models import PaymentConfirmation
from .utils import get_valid_keys, validate_response_code


@method_decorator(csrf_exempt, "dispatch")
class ConfirmationView(View):
    def post(self, request, *args, **kwargs):
        data = {}
        for k, v in request.POST.items():
            if k in ("x_id_factura", "x_respuesta", "x_fecha_transaccion", "x_cod_respuesta"):
                # Ignore fields in both English and Spanish
                continue
            data[k.replace("x_", "")] = v
        # TODO: Validate name consistency across all abstract models to prevent things like: id_user and customer_id.
        # Invert invoice name to keep the names consistent
        data["invoice_id"] = data["id_invoice"]
        del data["id_invoice"]

        # Get boolean fron the test_request attribute
        data["test_request"] = data["test_request"] == "TRUE"
        data["raw"] = json.dumps(request.POST)

        # Validate there are no new fields.
        # Epayco usually adds new fields without any notice.
        valid_keys = get_valid_keys()
        data = {k: v for k, v in data.items() if k in valid_keys}

        # The AbstractFlagSegment's model's save method does the flagging validations.
        item = PaymentConfirmation.objects.create(**data)
        return JsonResponse({"flag": item.is_flagged}, status=200)


@method_decorator(csrf_exempt, "dispatch")
class ResponseValidationView(TemplateView):
    template_name = "simple_payment_response.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        ref = self.request.GET.get("ref_payco")
        validation = validate_response_code(ref, self.request)
        context["payment"] = validation
        return context

    def post(self, request, **kwargs):
        ref = request.POST.get("x_ref_payco", None)
        if ref is None:
            return JsonResponse({"ref": ["This field is required."]}, status=400)
        validate_response_code(ref, request)
        return HttpResponseRedirect(reverse("epayco_response_validation") + "?ref_payco={}".format(ref))
