# Generated by Django 3.0 on 2019-12-22 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orloveFurniture', '0003_auto_20191222_1928'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RequiredMaterials',
            new_name='RequiredMaterial',
        ),
        migrations.RenameModel(
            old_name='RequiredOperations',
            new_name='RequiredOperation',
        ),
    ]
