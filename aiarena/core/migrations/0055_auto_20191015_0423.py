# Generated by Django 2.1.7 on 2019-10-14 17:53

import aiarena.core.models
import aiarena.core.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20191012_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='file',
            field=models.FileField(storage=aiarena.core.storage.OverwriteStorage(), upload_to=aiarena.core.models.map_file_upload_to),
        ),
    ]