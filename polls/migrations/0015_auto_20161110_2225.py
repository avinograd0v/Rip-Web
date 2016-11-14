# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 19:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20161110_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='approved_by',
            field=models.ManyToManyField(related_name='answers_approved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='disapproved_by',
            field=models.ManyToManyField(related_name='answers_disapproved', to=settings.AUTH_USER_MODEL),
        ),
    ]
