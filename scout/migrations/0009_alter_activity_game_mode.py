# Generated by Django 4.1.7 on 2023-08-29 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0008_alter_activity_required_materials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='game_mode',
            field=models.CharField(choices=[('team', 'Team'), ('unit', 'Unit'), ('single', 'Single')], default='team', max_length=80),
        ),
    ]
