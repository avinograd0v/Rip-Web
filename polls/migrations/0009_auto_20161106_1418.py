# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20161106_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='../media/default-user.png', upload_to=''),
        ),
    ]