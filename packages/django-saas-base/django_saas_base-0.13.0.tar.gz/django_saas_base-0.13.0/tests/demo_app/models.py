from django.db import models
from saas_base.db.fields import EncryptedField


class UserSecret(models.Model):
    secret_key = EncryptedField(null=True, blank=True)
