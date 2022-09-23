|PyPI latest| |TravisCI|

About
-----

Pretty UID fields for your Django models, with customizable prefixes and
controlled length. Tested vs. Python 3.5, 3.6, 3.7, 3.8, 3.9, 3.10 and
Django 2.2, 3.1, 3.2, 4.0, 4.1.


Usage
-----

See examples below. You can optionally inherit your models from `UIDModel`,
which gracefully handles IntegrityError on saving UIDs, making up to 3 attempts
with random UIDs. Integrity errors should be pretty rare if you use large enough
`max_length` on your fields, but you may still want to use it for extra safety::

    from django_uidfield.fields import UIDField

    class YourModel(models.Model):
        uid_field = UIDField(prefix='tmp_', max_length=20)

    # the value will be like 'tmp_Akw81LmtPqS93dKb'

or::

    from django_uidfield.models import UIDModel
    from django_uidfield.fields import UIDField


    class YourModel(UIDModel):
        uid_field = UIDField(prefix='tmp_', max_length=20)


Adding a UIDField to an existing model
--------------------------------------

You can populate the field with a data-migration::

    def populate_uid(apps, schema_editor):
        User = apps.get_model("users", "User")

        for user in User.objects.all():
            user._meta.get_field("uid").populate(user, force_renew=True)
            user.save()


    class Migration(migrations.Migration):
        operations = [migrations.RunPython(code=populate_uid)]

Note that the 3-attempt deduplication mechanism will not work, and you can get
an error if you have a lot of objects and a small max_length.


`Changelog <CHANGELOG.rst>`_

.. |PyPI latest| image:: https://img.shields.io/pypi/v/django-uidfield.svg?maxAge=120
   :target: https://pypi.python.org/pypi/django-uidfield
.. |TravisCI| image:: https://travis-ci.org/ivelum/django-uidfield.svg?branch=master
   :target: https://travis-ci.org/ivelum/django-uidfield
