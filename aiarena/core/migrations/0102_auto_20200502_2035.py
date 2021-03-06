# Generated by Django 2.1.7 on 2020-05-02 11:05

import aiarena.core.models.bot
import aiarena.core.storage
from django.db import migrations
import private_storage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0101_auto_20200502_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='bot_data',
            field=private_storage.fields.PrivateFileField(blank=True, null=True, storage=aiarena.core.storage.OverwritePrivateStorage(base_url='/'), upload_to=aiarena.core.models.bot.bot_data_upload_to),
        ),
    ]
