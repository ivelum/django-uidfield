|PyPI latest| |TravisCI|

About
-----

Pretty UID fields for your Django models, with customizable prefixes and controlled length. Tested vs. Python 2.7, 3.5, 3.6 and Django 1.8 - 1.11.


Usage
-----

See examples below. You can optionally inherit your models from `UIDModel`, which gracefully handles IntegrityError on saving UIDs, making up to 3 attempts with random UIDs. Integrity errors should be pretty rare if you use large enough `max_length` on your fields, but you may still want to use it for extra safety::

    from django_uidfield.fields import UIDField

    class YourModel(models.Model):
        uid_field = UIDField(prefix='tmp_', max_length=20)

    # the value will be like 'tmp_Akw81LmtPqS93dKb'

or::

    from django_uidfield.models import UIDModel
    from django_uidfield.fields import UIDField


    class YourModel(UIDModel):
        uid_field = UIDField(prefix='tmp_', max_length=20)

Changelog
---------

0.2.0
=====
* [BREAKING] UID fields defined as nullable will stop populate their value on
  the new model instance saving. If your code relied on the old behavior, please
  make sure that all your UID fields don't have the `null=True` attribute or
  populate their values manually in save or in calling code.

* [BREAKING] Drop support for Django 1.8, 1.10, 1.11

* [BREAKING] Drop support for Python 2.7

* add support for Django 2.2, and 3.0 versions and Python 3.7, and 3.8 versions


.. |PyPI latest| image:: https://img.shields.io/pypi/v/django-uidfield.svg?maxAge=120
   :target: https://pypi.python.org/pypi/django-reversion
.. |TravisCI| image:: https://travis-ci.org/ivelum/django-uidfield.svg?branch=master
   :target: https://travis-ci.org/ivelum/django-uidfield
