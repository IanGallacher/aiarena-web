# Generated by Django 2.1.7 on 2019-10-05 16:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_remove_bot_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='bot_zip_updated',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
            preserve_default=False,
        ),
    ]
