# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 19:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_answer_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='polls.User'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='polls.User'),
        ),
    ]