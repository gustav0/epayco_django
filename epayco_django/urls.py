try:
    from django.urls import re_path
except:
    from django.conf.urls import url as re_path

from .views import ConfirmationView, ResponseValidationView

# app_name = 'epayco_django' # If i include this it will not find the urls.
urlpatterns = [
    re_path(
        "^epayco/confirmation$", ConfirmationView.as_view(), name="epayco_confirmation"
    ),
    re_path(
        "^payment/response-validation$",
        ResponseValidationView.as_view(),
        name="epayco_response_validation",
    ),
]
