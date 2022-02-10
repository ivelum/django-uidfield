import re

from django.db.transaction import atomic
from django.test import TestCase, TransactionTestCase, override_settings

from .fields import UIDField
from .models import UIDModel

FIELD_RE = re.compile('[a-z]{3}_[A-Za-z0-9]{16}')


class TestModel(UIDModel):
    uid_field = UIDField(prefix='tmp_', max_length=20, unique=True)
    nullable_uid_field = UIDField(
        prefix='nul_',
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )


class TestModelWithPk(UIDModel):
    id = UIDField(primary_key=True, prefix='pk_', max_length=20)


class TestDbRouterDefault:
    def db_for_read(self, model, **hints):
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'


class TestDbRouterOther:
    def db_for_read(self, model, **hints):
        return 'other'

    def db_for_write(self, model, **hints):
        return 'other'


class CheckMixin:
    def _check_field_value(self, value):
        self.assertEqual(len(value), 20)
        self.assertNotEquals(FIELD_RE.match(value), None)


class UIDFieldTest(CheckMixin, TestCase):
    """UIDField Wrapper Tests"""

    def test_uid_field_value_generate(self):
        """Test generating an UID value in UIDField"""
        obj = TestModel.objects.create()
        new_obj = TestModel.objects.get(id=obj.id)
        self._check_field_value(new_obj.uid_field)

    def test_nullable_uid_field_value_stays_nullable(self):
        """Test generating an UID value in UIDField"""
        obj = TestModel.objects.create()
        new_obj = TestModel.objects.get(id=obj.id)
        self.assertIsNone(new_obj.nullable_uid_field)

    def test_uid_field_value_regeneration(self):
        """Test regenerating an UID value in UIDField"""
        first_obj = TestModel.objects.create()
        second_obj = TestModel(uid_field=first_obj.uid_field)
        second_obj.save()
        self._check_field_value(second_obj.uid_field)
        self.assertNotEquals(first_obj.uid_field, second_obj.uid_field)

    def test_uidfield_as_pk(self):
        """Test usage of UIDField as primary key"""
        obj = TestModelWithPk.objects.create()
        self.assertTrue(obj.pk.startswith('pk_'))
        TestModelWithPk.objects.create()
        another_copy_of_obj = TestModelWithPk.objects.get(pk=obj.pk)
        self.assertEqual(obj, another_copy_of_obj)


class UIDFieldMultidbTest(CheckMixin, TransactionTestCase):
    databases = {'default', 'other'}

    def test_uid_recreation_with_explicit_routing(self):
        """
        Test regenerating an UID value in UIDField in correct DB
        with explicit routing
        """
        for db in {'default', 'other'}:
            # it is important to start transaction outside the create/save
            # methods to check that it is not broken by incorrectly created
            # inner transactions
            with atomic(using=db):
                first_obj = TestModel.objects.using(db).create()
                second_obj = TestModel(uid_field=first_obj.uid_field)
                second_obj.save(using=db)
                self._check_field_value(second_obj.uid_field)
                self.assertNotEquals(first_obj.uid_field, second_obj.uid_field)

    def test_uid_recreation_with_route_based_routing(self):
        """
        Test regenerating an UID value in UIDField in correct DB.
        Routing is based on DB router.
        """
        for db in {'default', 'other'}:
            # route all queries to the selected DB. the save method should
            # correctly determine correct DB where to open transaction
            router = 'django_uidfield.tests.TestDbRouter{db}'.format(
                db=db.capitalize(),
            )
            with atomic(using=db), override_settings(DATABASE_ROUTERS=[router]):
                first_obj = TestModel.objects.create()
                second_obj = TestModel(uid_field=first_obj.uid_field)
                second_obj.save()
                self._check_field_value(second_obj.uid_field)
                self.assertNotEquals(first_obj.uid_field, second_obj.uid_field)
