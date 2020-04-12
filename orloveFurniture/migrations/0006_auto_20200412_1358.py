# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-04-12 13:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orloveFurniture', '0005_auto_20200208_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workercatalog',
            name='idWorker',
        ),
        migrations.AlterField(
            model_name='requiredmaterial',
            name='idOrder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orloveFurniture.Order'),
        ),
        migrations.AlterField(
            model_name='requiredoperationcontractor',
            name='idOrder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orloveFurniture.Order'),
        ),
        migrations.AlterField(
            model_name='requiredoperationmanufactory',
            name='idOrder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orloveFurniture.Order'),
        ),
        migrations.AlterField(
            model_name='requiredoperationproject',
            name='idOrder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orloveFurniture.Order'),
        ),
    ]
