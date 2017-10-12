import re

from django.db import models
from django.test import TestCase

from .fields import UIDField
from .models import UIDModel

FIELD_RE = re.compile('[a-z]{3}_[A-Za-z0-9]{16}')


class TestModel(UIDModel):
    uid_field = UIDField(prefix='tmp_', max_length=20, unique=True)


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

    def test_uid_field_value_regeneration(self):
        """Test regenerating an UID value in UIDField"""
        obj = TestModel.objects.create()
        first_obj = TestModel.objects.get(id=obj.id)
        second_obj = TestModel(uid_field=first_obj.uid_field)
        second_obj.save()
        self._check_field_value(second_obj.uid_field)
        self.assertNotEquals(first_obj.uid_field, second_obj.uid_field)
