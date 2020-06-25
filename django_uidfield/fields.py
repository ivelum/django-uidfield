import string

from django.db import models

from .misc import new_uid


class UIDField(models.CharField):
    prefix = None
    chars = None

    def __init__(self, prefix=None, chars=string.ascii_letters + string.digits,
                 *args, **kwargs):
        self.prefix = prefix
        self.chars = chars
        super(UIDField, self).__init__(*args, **kwargs)

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
