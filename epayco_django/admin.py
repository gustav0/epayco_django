from django.contrib import admin

from .models import PaymentConfirmation


class PaymentConfirmationAdmin(admin.ModelAdmin):
    list_display = ("ref_payco", "transaction_state", "test_request", "flag", "flag_info", "created")
    list_filter = ("flag", "test_request", "transaction_state")
    search_fields = ["transaction_id", "ref_payco"]

    fieldsets = (
        (None, {"fields": ("invoice_id", "ref_payco", "description")}),
        (
            "Payment",
            {
                "classes": ("collapse",),
                "fields": ("amount", "amount_country", "amount_ok", "amount_base", "tax", "currency_code"),
            },
        ),
        ("Card", {"classes": ("collapse",), "fields": ("cardnumber", "quotas")}),
        (
            "Transaction",
            {
                "classes": ("collapse",),
                "fields": (
                    "transaction_id",
                    "transaction_state",
                    "bank_name",
                    "response",
                    "approval_code",
                    "transaction_date",
                    "cod_response",
                    "response_reason_text",
                    "errorcode",
                    "cod_transaction_state",
                    "business",
                    "franchise",
                ),
            },
        ),
        (
            "Customer",
            {
                "classes": ("collapse",),
                "fields": (
                    "cust_id_cliente",
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
                ),
            },
        ),
        (
            "Extra",
            {
                "classes": ("collapse",),
                "fields": (
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
                ),
            },
        ),
        (
            "Admin",
            {
                "classes": ("collapse",),
                "fields": ("signature", "test_request", "flag", "flag_code", "flag_info", "raw"),
            },
        ),
    )


admin.site.register(PaymentConfirmation, PaymentConfirmationAdmin)
