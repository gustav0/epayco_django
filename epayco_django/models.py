from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .settings import epayco_settings
from .signals import (
    invalid_confirmation_received,
    confirmation_was_flagged,
    valid_confirmation_received,
    confirmation_was_approved,
    confirmation_was_rejected,
)
from .utils import get_signature


class AbstractFlagSegment(models.Model):
    DUPLICATE_TRANSACTION = "1001"
    INVALID_SIGN = "1002"
    TEST_TRANSACTION = "1003"
    FLAG_CODES = (
        (DUPLICATE_TRANSACTION, "Duplicate Transaction"),
        (INVALID_SIGN, "Invalid Sign"),
        (TEST_TRANSACTION, "Test transacción on non test environment"),
    )
    flag = models.BooleanField(default=False)
    flag_code = models.CharField(max_length=4, choices=FLAG_CODES, default="", blank=True)
    flag_info = models.CharField(max_length=100, default="", blank=True)

    class Meta:
        abstract = True

    @property
    def is_flagged(self):
        return self.flag

    def save(self, *args, **kwargs):
        # transaction_id can be found at 'AbstractTransactionSegment'
        if not self.id:
            signature = get_signature(
                self.cust_id_cliente,
                epayco_settings.P_KEY,
                self.ref_payco,
                self.transaction_id,
                self.amount,
                self.currency_code,
            )
            valid_signature = signature == self.signature
            if not valid_signature:
                self.flag = True
                self.flag_code = self.INVALID_SIGN
                self.flag_info = "Invalid sign. ({}...)".format(self.signature[:18])
                super().save(*args, **kwargs)
                return
        exists = (
            PaymentConfirmation.objects.filter(transaction_id=self.transaction_id)
            .exclude(cod_transaction_state=3)
            .exists()
        )  # Pending transaction shouldn't be flagged

        if not self.id and exists:  # Duplicate transaction validation
            self.flag = True
            self.flag_code = self.DUPLICATE_TRANSACTION
            self.flag_info = "Duplicate transaction_id. ({})".format(self.transaction_id)

        if not self.id and self.test_request and not epayco_settings.TEST:  # Duplicate transaction validation
            self.flag = True
            self.flag_code = self.TEST_TRANSACTION
            self.flag_info = "Test transaction on non test environment. ({})".format(self.transaction_id)
        super().save(*args, **kwargs)


class AbstractPaymentSegment(models.Model):
    amount = models.CharField(max_length=32)
    amount_country = models.CharField(max_length=32)
    amount_ok = models.CharField(max_length=32)
    tax = models.CharField(max_length=32)
    amount_base = models.CharField(max_length=32)
    currency_code = models.CharField(max_length=4)

    class Meta:
        abstract = True


class AbstractCreditCardSegment(models.Model):
    cardnumber = models.CharField(max_length=32)
    quotas = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        try:
            self.quotas = int(self.quotas)
        except ValueError:
            self.quotas = 0
        super().save(*args, **kwargs)


class AbstractTransactionSegment(models.Model):
    transaction_id = models.CharField(max_length=64)
    transaction_state = models.CharField(max_length=32)
    bank_name = models.CharField(max_length=128)
    response = models.CharField(max_length=32)
    approval_code = models.CharField(max_length=32)
    transaction_date = models.CharField(max_length=32)
    cod_response = models.CharField(max_length=32)
    response_reason_text = models.CharField(max_length=256)
    errorcode = models.CharField(max_length=32)
    cod_transaction_state = models.CharField(max_length=32)
    business = models.CharField(max_length=256)
    franchise = models.CharField(max_length=32)

    class Meta:
        abstract = True

    def __str__(self):
        return self.transaction_id

    @property
    def is_approved(self):
        return self.cod_transaction_state == "1"

    @property
    def is_rejected(self):
        return self.cod_transaction_state == "2"

    @property
    def is_pending(self):
        return self.cod_transaction_state == "3"

    @property
    def is_failed(self):
        return self.cod_transaction_state == "4"

    @property
    def is_reversed(self):
        return self.cod_transaction_state == "6"

    @property
    def is_retained(self):
        return self.cod_transaction_state == "7"

    @property
    def is_initiated(self):
        return self.cod_transaction_state == "8"

    @property
    def is_expired(self):
        return self.cod_transaction_state == "9"

    @property
    def is_abandoned(self):
        return self.cod_transaction_state == "10"

    @property
    def is_canceled(self):
        return self.cod_transaction_state == "11"

    @property
    def is_antifraud_flagged(self):
        return self.cod_transaction_state == "12"


class AbstractCustomerSegment(models.Model):
    cust_id_cliente = models.CharField(max_length=128)
    customer_doctype = models.CharField(max_length=12)
    customer_document = models.CharField(max_length=64)
    customer_name = models.CharField(max_length=128)
    customer_lastname = models.CharField(max_length=128)
    customer_email = models.CharField(max_length=128)
    customer_phone = models.CharField(max_length=32)
    customer_movil = models.CharField(max_length=32)
    customer_ind_pais = models.CharField(max_length=32)
    customer_country = models.CharField(max_length=32)
    customer_city = models.CharField(max_length=32)
    customer_address = models.TextField()
    customer_ip = models.CharField(max_length=16)

    class Meta:
        abstract = True


class AbstractPaymentConfirmation(
    AbstractCustomerSegment,
    AbstractTransactionSegment,
    AbstractCreditCardSegment,
    AbstractFlagSegment,
    AbstractPaymentSegment,
):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class PaymentConfirmation(AbstractPaymentConfirmation):
    invoice_id = models.CharField(max_length=128)
    ref_payco = models.CharField(max_length=128)
    signature = models.CharField(max_length=256)
    description = models.TextField()

    test_request = models.BooleanField()

    extra1 = models.CharField(max_length=255, blank=True)
    extra2 = models.CharField(max_length=255, blank=True)
    extra3 = models.CharField(max_length=255, blank=True)
    extra4 = models.CharField(max_length=255, blank=True)
    extra5 = models.CharField(max_length=255, blank=True)
    extra6 = models.CharField(max_length=255, blank=True)
    extra7 = models.CharField(max_length=255, blank=True)
    extra8 = models.CharField(max_length=255, blank=True)
    extra9 = models.CharField(max_length=255, blank=True)
    extra10 = models.CharField(max_length=255, blank=True)

    raw = models.TextField()

    class Meta:
        db_table = "epayco_payment_confirmation"

    def get_invoice_data(self):
        return {
            "invoice": self.invoice_id,
            "ref_payco": self.ref_payco,
            "description": self.description,
            "amount": self.amount,
            "impuesto": self.tax,
            "base_impuesto": self.amount_base,
            "response_reason": self.response_reason_text,
            "error_code": self.errorcode,
            "nombre_pagador": self.customer_name,
            "apellido_pagador": self.customer_lastname,
        }


@receiver(post_save, sender=PaymentConfirmation)
def payment_confirmation_save(sender, instance, created, **kwargs):
    if created:
        if instance.is_flagged:
            invalid_confirmation_received.send(sender=PaymentConfirmation, confirmation=instance)
            confirmation_was_flagged.send(sender=PaymentConfirmation, confirmation=instance)
        else:
            valid_confirmation_received.send(sender=PaymentConfirmation, confirmation=instance)
            if instance.is_approved:
                confirmation_was_approved.send(sender=PaymentConfirmation, confirmation=instance)
            elif instance.is_rejected:
                confirmation_was_rejected.send(sender=PaymentConfirmation, confirmation=instance)
