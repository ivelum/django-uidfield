0.2.0 (unreleased yet)
-----------------------
* [BREAKING] UID fields defined as nullable will stop populate their value on 
the new model instance saving. If your code relied on the old behavior, please
make sure that all your UID fields don't have the `null=True` attribute or 
populate their values manually in save or in calling code.

* [BREAKING] Drop support for Django 1.8, 1.10, 1.11
 
* [BREAKING] Drop support for Python 2.7

* add support for Django 2.2, and 3.0 versions and Python 3.7, and 3.8 versions
