# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-01-26 15:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orloveFurniture', '0015_auto_20200125_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requiredmaterial',
            name='idOrder',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='orloveFurniture.Order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requiredoperation',
            name='idOrder',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='orloveFurniture.Order'),
            preserve_default=False,
        ),
    ]