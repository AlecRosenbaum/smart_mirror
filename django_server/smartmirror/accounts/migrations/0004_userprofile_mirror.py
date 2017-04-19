# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-14 06:06
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_ical_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='mirror',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
