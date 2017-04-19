# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-14 06:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_ical_link'),
        ('display', '0002_auto_20170414_0450'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortMirror',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_id', models.CharField(max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile')),
            ],
        ),
        migrations.RemoveField(
            model_name='calendar',
            name='user',
        ),
        migrations.RemoveField(
            model_name='mirror',
            name='user',
        ),
        migrations.DeleteModel(
            name='Calendar',
        ),
        migrations.DeleteModel(
            name='Mirror',
        ),
    ]
