# Generated by Django 2.1.7 on 2019-11-11 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_auto_20191110_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_matches', to=settings.AUTH_USER_MODEL),
        ),
    ]
