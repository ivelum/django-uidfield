import re

from django.test import TestCase

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


class UIDFieldTest(TestCase):
    """UIDField Wrapper Tests"""

    def _check_field_value(self, value):
        self.assertEqual(len(value), 20)
        self.assertNotEquals(FIELD_RE.match(value), None)

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
        obj = TestModel.objects.create()
        first_obj = TestModel.objects.get(id=obj.id)
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
