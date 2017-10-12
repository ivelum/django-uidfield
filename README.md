[![Build Status](https://secure.travis-ci.org/ivelum/django-uidfield.png)](http://travis-ci.org/ivelum/django-uidfield)
[![PyPI version](https://badge.fury.io/py/django-uidfield.svg)](https://badge.fury.io/py/django-uidfield)

About
-----

Pretty UID fields for your Django models, with customizable prefixes and controlled length. Tested vs. Python 2.7, 3.5, 3.6 and Django 1.8 - 1.11.


Usage
-----

See examples below. You can optionally inherit your models from `UIDModel`, which gracefully handles IntergrityError on saving UIDs, making up to 3 attempts with random UIDs. Integrity errors should be pretty rare if you use large enough `max_length` on your fields, but you may still want to use it for extra safety.

```python
from django_uidfield.fields import UIDField


class YourModel(models.Model):
    uid_field = UIDField(prefix='tmp_', max_length=20)
    
# the value will be like 'tmp_Akw81LmtPqS93dKb'
```
or
```python
from django_uidfield.models import UIDModel
from django_uidfield.fields import UIDField


class YourModel(UIDModel):
    uid_field = UIDField(prefix='tmp_', max_length=20)
```
