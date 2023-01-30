import string

from django.db import models

from .misc import new_uid


class UIDField(models.CharField):
    prefix = None
    chars = None

    def __init__(
        self,
        prefix=None,
        chars=string.ascii_letters + string.digits,
        alternative_prefixes=None,
        *args,
        **kwargs
    ):
        if alternative_prefixes is None:
            alternative_prefixes = []
        self.alternative_prefixes = alternative_prefixes
        self.prefix = prefix
        self.chars = chars
        super(UIDField, self).__init__(*args, **kwargs)

    @property
    def non_db_attrs(self):
        return super().non_db_attrs + (
            'prefix',
            'chars',
            'alternative_prefixes',
        )

    def populate(self, model_instance, force_renew=False):
        uid = getattr(model_instance, self.attname, None)
        if (not uid and not self.null) or force_renew:
            uid = new_uid(self.max_length, prefix=self.prefix, chars=self.chars)
            setattr(model_instance, self.attname, uid)
        return uid

    def pre_save(self, model_instance, add):
        if add:
            return self.populate(model_instance)
        else:
            return getattr(model_instance, self.attname)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.prefix:
            kwargs['prefix'] = self.prefix
        if self.alternative_prefixes:
            kwargs['alternative_prefixes'] = self.alternative_prefixes
        kwargs['chars'] = self.chars
        return name, path, args, kwargs

    def get_prep_value(self, value):
        value = super().get_prep_value(value)

        for alt_prefix in self.alternative_prefixes:
            if not value.startswith(alt_prefix):
                continue

            prefix_length = len(alt_prefix)
            _, data = value[:prefix_length], value[prefix_length:]
            value = self.prefix + data
            break

        return value
