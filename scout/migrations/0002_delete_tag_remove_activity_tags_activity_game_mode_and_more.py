# Generated by Django 4.1.7 on 2023-08-21 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='tags',
        ),
        migrations.AddField(
            model_name='activity',
            name='game_mode',
            field=models.CharField(choices=[('T', 'TEAM'), ('U', 'UNIT'), ('S', 'SINGLE')], default='T', max_length=1),
        ),
        migrations.AddField(
            model_name='activity',
            name='is_suitable_for_disabled',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.CharField(choices=[('ID', 'indoor activity'), ('OD', 'outdoor activity'), ('OL', 'online activity'), ('IP', 'in-person activity')], default='OD', max_length=2),
        ),
        migrations.AlterField(
            model_name='activity',
            name='age_range',
            field=models.CharField(choices=[('L', 'Lupetti'), ('E', 'Esploratori'), ('R', 'Rover')], default='L', max_length=1),
        ),
    ]
