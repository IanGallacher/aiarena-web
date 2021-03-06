# Generated by Django 3.0.8 on 2020-10-31 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0116_user_sync_patreon_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.TextField(blank=True, max_length=20, null=True)),
                ('text', models.TextField(max_length=500)),
                ('yt_link', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
