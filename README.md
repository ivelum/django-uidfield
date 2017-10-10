[![Build Status](https://secure.travis-ci.org/ivelum/django-uidfield.png)](http://travis-ci.org/ivelum/django-uidfield)

Introduction
------------

Django-uidfield is a package which includes class UIDField for models.

It allows you to create unique string fields with any length and any fixed prefix.


Usage
-----
```python
class YourModel(models.Model):
    uid_field = UIDField(prefix='tmp_', max_length=20)
    
# the value will be like 'tmp_Akw81LmtPqS93dKb'
```
