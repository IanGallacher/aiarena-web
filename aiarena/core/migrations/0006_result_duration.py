# Generated by Django 2.1.7 on 2019-04-26 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190426_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='duration',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
