# Generated by Django 3.0 on 2020-01-06 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orloveFurniture', '0005_auto_20191222_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
