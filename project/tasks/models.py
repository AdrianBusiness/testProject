# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    opened = models.ForeignKey(User, related_name='opened')
    closed = models.ForeignKey(User, null=True, related_name='closed')
