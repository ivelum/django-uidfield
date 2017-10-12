from django.db import models, IntegrityError, transaction

from .fields import UIDField


class UIDModel(models.Model):
    max_save_attempts = 3

    class Meta:
        abstract = True

    def uid_fields(self):
        return [f for f in self._meta.fields if isinstance(f, UIDField)]

    def populate_uid_fields(self, force_renew=False, uid_fields=None):
        for field in uid_fields or self.uid_fields():
            field.populate(self, force_renew=force_renew)

    def save(self, *args, **kwargs):
        for save_attempt in range(self.max_save_attempts):
            try:
                with transaction.atomic():
                    return super(UIDModel, self).save(*args, **kwargs)
            except IntegrityError as e:
                uid_fields = self.uid_fields()
                if not any(field.attname in str(e) for field in uid_fields):
                    raise
                if save_attempt < self.max_save_attempts - 1:
                    self.populate_uid_fields(
                        force_renew=True, uid_fields=uid_fields
                    )
        raise IntegrityError('Failed to save %s with unique UID fields' % self)
