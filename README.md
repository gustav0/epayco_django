# ePayco Django

A Django integration for ePayco's gateway.
##Requirements
* [Python](https://www.python.org/) (3.5, 3.6, 3.7, 3.8)
* [Django](https://github.com/django/django)
* [epayco-python](https://github.com/epayco/epayco-python)

## Installation
If you want clone the repository:
```
$ git clone https://github.com/gustav0/epayco_django.git
```

Install from package manager
```
$ pip install epayco-django
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
    'CONFIRMATION_URL': reverse('epayco_confirmation'),
    'RESPONSE_URL': reverse('epayco_response'),
    
    # And you can use your own image as a payment button
    'CHECKOUT_BUTTON_URL': 'https://mydomain.com/btns/pay_now_button.png'
}
```
Now edit the `myproject/urls.py` module in your project:

```
from django.conf.urls import url, include
from epayco_django import urls as epayco_urls

urlpatterns = [
    ...
    url('^epayco/', include(epayco_urls, namespace='epayco')),
    ...
]
```
Or if you are running django 2.0+
```
from django.urls import path, include
from epayco_django import urls as epayco_urls

urlpatterns = [
    ...
    path('epayco/', include(epayco_urls, namespace='epayco')),
    ...
]
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

Now that you set payment confirmations to be reported to your site, we can listen 
to whatever confirmation is sent, validate it and act on it. Listen to any of the 
`epayco_django.signals` you are interested in and you should be able to acomplish 
what you need. Here is an example:
```
from django.dispatch import receiver
from epayco_django.signals import valid_confirmation_received

@receiver(valid_confirmation_received)
def activate_membership(sender, user=None, **kwargs):
    ...
    HERE SHOULD BE YOUR MEMBERSHIP ACTIVATION CODE
    ...
```



## Contributing
I'm always grateful for any kind of contribution including but not limited to bug 
reports, code enhancements, bug fixes, and even functionality suggestions.

##### You can report any bug you find or suggest new functionality with a new 
[issue](https://github.com/gustav0/epayco_django/issues).

##### If you want to add yourself some functionality to the wrapper:
1. Fork it ( https://github.com/gustav0/epayco_django)
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Adds my new feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request