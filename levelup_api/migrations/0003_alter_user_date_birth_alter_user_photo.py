# Generated by Django 4.0.4 on 2022-05-17 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelup_api', '0002_remove_user_groups_remove_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]