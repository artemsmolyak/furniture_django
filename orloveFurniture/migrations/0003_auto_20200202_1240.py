# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-02 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orloveFurniture', '0002_auto_20200202_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requiredoperationcontractor',
            name='isDone',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='requiredoperationcontractor',
            name='isDoneDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requiredoperationmanufactory',
            name='isDone',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='requiredoperationmanufactory',
            name='isDoneDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requiredoperationproject',
            name='isDone',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='requiredoperationproject',
            name='isDoneDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
