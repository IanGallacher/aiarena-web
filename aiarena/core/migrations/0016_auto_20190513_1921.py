# Generated by Django 2.1.7 on 2019-05-13 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_bot_current_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='current_match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bots_currently_in_match', to='core.Match'),
        ),
    ]
