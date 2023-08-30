# Generated by Django 4.1.7 on 2023-08-30 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0009_alter_activity_game_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='location',
            field=models.CharField(choices=[('indoor', 'indoor activity'), ('outdoor', 'outdoor activity'), ('online', 'online activity'), ('in-person', 'in-person activity')], default='outdoor', max_length=80),
        ),
    ]
