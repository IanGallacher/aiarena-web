# Generated by Django 2.1.7 on 2019-10-10 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_merge_20191011_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='type',
            field=models.CharField(choices=[('MatchCancelled', 'MatchCancelled'), ('InitializationError', 'InitializationError'), ('Error', 'Error'), ('Player1Win', 'Player1Win'), ('Player1Crash', 'Player1Crash'), ('Player1TimeOut', 'Player1TimeOut'), ('Player1RaceMismatch', 'Player1RaceMismatch'), ('Player1Surrender', 'Player1Surrender'), ('Player2Win', 'Player2Win'), ('Player2Crash', 'Player2Crash'), ('Player2TimeOut', 'Player2TimeOut'), ('Player2RaceMismatch', 'Player2RaceMismatch'), ('Player2Surrender', 'Player2Surrender'), ('Tie', 'Tie')], max_length=32),
        ),
    ]
