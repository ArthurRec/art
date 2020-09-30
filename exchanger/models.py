import datetime
import random

from django.db import models


class Exchange(models.Model):
    base = models.CharField(max_length=3, blank=False, null=False)
    date = models.DateField(db_index=True, default=datetime.date.today())
    goal = models.CharField(max_length=3, blank=False, null=False)
    rate = models.DecimalField(
        decimal_places=6, max_digits=14, default=random.random())

    class Meta:
        unique_together = ('base', 'date', 'goal', )
