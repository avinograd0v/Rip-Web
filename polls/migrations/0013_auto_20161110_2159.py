# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 18:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20161110_2158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='voted_up_by',
            new_name='approved_by',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='voted_down_by',
            new_name='disapproved_by',
        ),
    ]