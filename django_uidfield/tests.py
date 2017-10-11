import re

from django.db import models
from django.test import TestCase

from .fields import UIDField


class DemoModel(models.Model):
    uid_field = UIDField(prefix='tmp_', max_length=20)


class UIDFieldTest(TestCase):
    """UIDField Wrapper Tests"""

    demo_model = DemoModel

    def test_uid_field_value_generate(self):
        """Test generating an UID value in UIDField"""
        obj = self.demo_model.objects.create()
        new_obj = self.demo_model.objects.get(id=obj.id)

        p = re.compile('[a-z]{3}_[A-Za-z0-9]{16}')

        self.assertEqual(len(new_obj.uid_field), 20)
        self.assertNotEquals(p.match(new_obj.uid_field), None)
