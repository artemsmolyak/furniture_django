# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-01-19 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orloveFurniture', '0009_auto_20200119_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cost',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='prepayment',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
