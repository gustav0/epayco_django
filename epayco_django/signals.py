import django.dispatch

valid_confirmation_received = django.dispatch.Signal(providing_args=['confirmation'])
invalid_confirmation_received = django.dispatch.Signal(providing_args=['confirmation'])

confirmation_was_flagged = django.dispatch.Signal(providing_args=['confirmation'])
confirmation_was_approved = django.dispatch.Signal(providing_args=['confirmation'])
confirmation_was_rejected = django.dispatch.Signal(providing_args=['confirmation'])
