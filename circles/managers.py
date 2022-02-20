# Python
import random
from string import ascii_uppercase, digits
# Django
from django.db import models


class InvitationManager(models.Manager):
    def create(self, **kwargs):
        pool = ascii_uppercase + digits
        code = kwargs.get('code', ''.join(random.choices(pool, k=10)))
        while self.filter(code=code).exists():
            code = ''.join(random.choices(pool, k=10))
        kwargs['code'] = code
        return super(InvitationManager, self).create(**kwargs)
