# Generated by Django 3.0.8 on 2020-11-12 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0120_auto_20201112_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='competition',
            field=models.ManyToManyField(related_name='maps', to='core.Competition'),
        ),
    ]