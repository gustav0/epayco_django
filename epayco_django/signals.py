import django.dispatch

valid_confirmation_received = django.dispatch.Signal()
invalid_confirmation_received = django.dispatch.Signal()

confirmation_was_flagged = django.dispatch.Signal()
confirmation_was_approved = django.dispatch.Signal()
confirmation_was_rejected = django.dispatch.Signal()
