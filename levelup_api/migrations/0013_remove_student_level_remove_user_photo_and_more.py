# Generated by Django 4.0.4 on 2022-05-17 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelup_api', '0012_alter_level_level_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='level',
        ),
        migrations.RemoveField(
            model_name='user',
            name='photo',
        ),
        migrations.AlterField(
            model_name='speaking_exercise',
            name='grade',
            field=models.FloatField(default=None),
        ),
    ]