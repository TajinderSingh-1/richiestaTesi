# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 10:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0032_auto_20171005_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='azienda',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='codice',
        ),
        migrations.RemoveField(
            model_name='studente',
            name='matricola',
        ),
    ]