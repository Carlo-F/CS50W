# Generated by Django 4.1.7 on 2023-08-29 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0006_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='age_range',
            field=models.CharField(choices=[('lupetti', 'Lupetti'), ('esploratori', 'Esploratori'), ('rover', 'Rover')], default='lupetti', max_length=80),
        ),
        migrations.AlterField(
            model_name='activity',
            name='game_mode',
            field=models.CharField(choices=[('team', 'TEAM'), ('unit', 'UNIT'), ('single', 'SINGLE')], default='team', max_length=80),
        ),
        migrations.AlterField(
            model_name='activity',
            name='location',
            field=models.CharField(choices=[('indorr', 'indoor activity'), ('outdoor', 'outdoor activity'), ('online', 'online activity'), ('in-person', 'in-person activity')], default='outdoor', max_length=80),
        ),
    ]
