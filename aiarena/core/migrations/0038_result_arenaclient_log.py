# Generated by Django 2.1.7 on 2019-07-27 12:03

from django.db import migrations, models

from aiarena.core import models as core_models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20190726_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='arenaclient_log',
            field=models.FileField(blank=True, null=True, upload_to=core_models.result.arenaclient_log_upload_to),
        ),
    ]
