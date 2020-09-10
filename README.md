# ePayco Django

A Django integration for ePayco's gateway.
##Requirements
* [Python](https://www.python.org/) (3.5, 3.6, 3.7, 3.8)
* [Django](https://github.com/django/django)
* [epayco-python](https://github.com/epayco/epayco-python)

### Warning
This library intends to use a fork of the epayco-python as the current version published py its owner
doesn't work on pip, and you would have to fix it manually.
The only changes are a couple of lines on the MANIFEST.in to make the setup.py properly 
include all relevant directories within the repo.

You can check the fork [here](https://github.com/gustav0/epayco-python).


Run this after you install the library.
```
pip install git+https://github.com/gustav0/epayco-python.git --no-cache-dir -U
```
Or append it to your requirements.txt at the end of the file.
```
git+https://github.com/gustav0/epayco-python.git
```

This will be a temporary workaround until they fix the problem. 


## Installation
If you want clone the repository:
```
git clone https://github.com/gustav0/epayco_django.git
```

Install from package manager
```
pip install epayco-django
```


Add `'epayco_django'` to your `INSTALLED_APPS` setting.
```
INSTALLED_APPS = [
    ...
    'epayco_django',
    ...
]
```

And set this in your settings, you can get this data from your ePayco dashboard under **Integration > API keys**.

```
EPAYCO = {
    'PUBLIC_KEY': 'MY_PUBLIC_KEY',
    'PRIVATE_KEY': 'MY_PRIVATE_KEY',
    'P_KEY': 'MY_P_KEY',
    'TEST': True, # you probably want to test it first rigth?
    
    # Optional (ignore these if you want the default behaviour)
    'FORCE_HTTPS': False, # If you use https on your website you may want to enable this.
    'RESPONSE_URL': reverse('epayco_response'),
    'CONFIRMATION_URL': reverse('epayco_confirmation'),
    
    # Instead of reversing a project url you could just use any url instead:
    'CONFIRMATION_URL': 'https://yourdomain.com/epayco/confirmation', 
    
    # And you can use your own image as a payment button
    'CHECKOUT_BUTTON_URL': 'https://mydomain.com/btns/pay_now_button.png'
}
```
Now edit the `myproject/urls.py` module in your project:

```
from django.conf.urls import url, include
# Or Django 2.0 +
from django.urls import path, include

from epayco_django import urls as epayco_urls


urlpatterns = [
    ...
    url('^', include(epayco_urls)),
    
    # or Django 2.0 +
    
    path('', include(epayco_urls)),
    ...
]
```
Finally run the migrations:
```
python manage.py migrate epayco_django
```

## Usage
At the moment the usage of the library is very limited, but it can be helpful 
to receive and act upon payment confirmations.

If this is what you need then you should set the `confirmation url` under 
**Integrations > My site properties > Gateway options** in the ePayco dashboard to:

```
https://yourdomain.com/epayco/confirmation
```
It is important to use https, and if you are working locally you can use tools 
like [ngrok](https://ngrok.com/).


### Template tags
We have a templatetag to generate a payment button that is quick and easy to
implement. It also is very customisable, you can assign any variable that's
available on the epayco checkout page.

Here is an example of how to use it.

```
{% load epayco_checkout %}

<div class="my-button">
{% render_checkout amount=9999 name="Test payment" currency="COP" extra1=request.user.id extra2="membership-3" request=request %}
</div>
```
And that's it, you have a fully working payment button. This tag uses the image
you set in the settings `CHECKOUT_BUTTON_URL`.

You can check the complete list of options for this template tag
[here](https://github.com/gustav0/epayco_django/blob/master/epayco_django/templatetags/epayco_checkout.py).


### Default payment responses
We have a template that is shown by the default payment response validation view at
`https://example.com/payment/response-validation`.

You can override this and whatever you feel like. Just create a new template at:
`templates/simple_payment_response.html`


### Payment Confirmation

Now that you set payment confirmations to be reported to your site, we can listen
to whatever confirmation is sent, validate it and act on it. Listen to any of the
`epayco_django.signals` you are interested in and you should be able to acomplish 
what you need. Here is an example:
```
from django.dispatch import receiver
from epayco_django.signals import valid_confirmation_received

@receiver(valid_confirmation_received)
def activate_membership(sender, confirmation=None, **kwargs):
    ...
    HERE SHOULD BE YOUR MEMBERSHIP ACTIVATION CODE
    ...
```

### Validating responses
We provide a utility that will search for existing payments with the provided 
reference code, if it finds a payment it will retrieve its information but if 
it doesn't it will fetch the payment data and activate the payment confirmation 
process by itself.

```
...

from epayco_django.utils import validate_response_code

class MyView(TemplateView):
    ...
    
    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(request, *args, **kwargs)
        ref_code = request.GET.get('ref_code')
        result = validate_response_code(ref_code)
        # You will get a dict like this as a result
        # {'valid_ref': True, 'existed': True, 'flag': False, 'obj': <PaymentConfirmationObject>}

        # INSERT CUSTOM CODE HERE

        return context
```

## Contributing
I'm always grateful for any kind of contribution including but not limited to bug reports, code enhancements, bug fixes, and even functionality suggestions.

##### You can report any bug you find or suggest new functionality with a new [issue](https://github.com/gustav0/epayco_django/issues).

##### If you want to add yourself some functionality to the wrapper:
1. Fork it ( https://github.com/gustav0/epayco_django)
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Adds my new feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request
