0.3.4
-----
* add support for Python 3.11

0.3.3
-----

* Support Django 4.1.x
* Add the `non_db_attr` property to the UIDField to avoid no-op DB alter field updates
  (Django 4.1+)

0.3.2
-----

* use Django DB router capabilities to determine a correct DB when it isn't
  explicitly passed to the UIDModel.save method

0.3.1
-----

* fixed a bug when transactions were being started in the wrong database in the
  multi-db setup
* added django 4.0.x to the test matrix

0.3.0
-----

* [BREAKING] drop support for Django 3.0

* add support for Python 3.9 and 3.10

* add support for Django 3.2

* starting this version, migrations for UIDField include `prefix` and `chars`
  arguments, specific for the field type. They are required for proper field
  usage in data migrations. As a side effect of this update,
  the `makemigrations` command will generate AlterField migrations for all
  existing UID fields in the project after upgrading from earlier versions.
  These migrations won't perform any SQL queries, though.

0.2.0
-----
* [BREAKING] UID fields defined as nullable will stop populate their value on
  the new model instance saving. If your code relied on the old behavior, please
  make sure that all your UID fields don't have the `null=True` attribute or
  populate their values manually in save or in calling code.

* [BREAKING] Drop support for Django 1.8, 1.10, 1.11

* [BREAKING] Drop support for Python 2.7

* add support for Django 2.2, and 3.0 versions and Python 3.7, and 3.8 versions
