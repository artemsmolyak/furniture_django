# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-01-12 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orloveFurniture', '0003_auto_20200112_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='name',
        ),
        migrations.AddField(
            model_name='storage',
            name='idMaterial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orloveFurniture.MaterialCatalog'),
        ),
        migrations.AlterField(
            model_name='requiredmaterial',
            name='idOrder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orloveFurniture.Order'),
        ),
    ]
