# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-01-25 16:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orloveFurniture', '0011_auto_20200125_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requiredoperation',
            name='cost',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='requiredoperation',
            name='idOperation',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='orloveFurniture.OperationCatalog'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requiredoperation',
            name='idWorker',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='orloveFurniture.WorkerCatalog'),
            preserve_default=False,
        ),
    ]