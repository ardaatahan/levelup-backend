# Generated by Django 4.0.4 on 2022-05-17 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0014_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(db_index=True, max_length=60, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('username', models.CharField(db_index=True, max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_system_admin', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_language_native', models.BooleanField(default=False)),
                ('date_birth', models.DateField()),
                ('photo', models.ImageField(upload_to='')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('duration', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('weekly_plan', models.TextField()),
                ('enrollment', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Class_Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Forum_Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('reply_text', models.TextField()),
                ('reply_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('due_datetime', models.DateTimeField()),
                ('assign_datetime', models.DateTimeField()),
                ('grade', models.FloatField()),
                ('given_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.class')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_name', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_title', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request_Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_datetime', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
                ('additional_notes', models.TextField()),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Language_Native',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.TextField()),
                ('rating', models.FloatField()),
                ('speaks', models.ManyToManyField(db_table='levelup_api_speaks', to='levelup_api.language')),
            ],
        ),
        migrations.CreateModel(
            name='System_Admin',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Speaking_Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_link', models.TextField()),
                ('exercise_datetime', models.DateTimeField()),
                ('grade', models.FloatField()),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.language')),
                ('language_native', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.language_native')),
            ],
        ),
        migrations.CreateModel(
            name='Rate_Exercise_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('review', models.TextField()),
                ('rate_datetime', models.DateTimeField()),
                ('speaking_exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.speaking_exercise')),
            ],
        ),
        migrations.CreateModel(
            name='Rate_Class_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('rate_datetime', models.DateTimeField()),
                ('given_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.class')),
            ],
        ),
        migrations.CreateModel(
            name='Forum_Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
                ('topic_title', models.TextField()),
                ('topic_text', models.TextField()),
                ('tags', models.ManyToManyField(db_table='levelup_api_topic_tags', to='levelup_api.tag')),
                ('topic_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Forum_Reply_Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('comment_text', models.TextField()),
                ('comment_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.forum_reply')),
            ],
        ),
        migrations.AddField(
            model_name='forum_reply',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.forum_topic'),
        ),
        migrations.AddField(
            model_name='class',
            name='books',
            field=models.ManyToManyField(db_table='levelup_api_require_books', to='levelup_api.class_book'),
        ),
        migrations.AddField(
            model_name='class',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.language'),
        ),
        migrations.AddField(
            model_name='class',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.level'),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.TextField()),
                ('rating', models.FloatField()),
                ('yearsOfExperience', models.IntegerField()),
                ('languages', models.ManyToManyField(db_table='levelup_api_knows', to='levelup_api.language')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('contact_no', models.CharField(max_length=12)),
                ('classes', models.ManyToManyField(db_table='levelup_api_takes', related_name='classes', to='levelup_api.class')),
                ('homeworks', models.ManyToManyField(db_table='levelup_api_get_hw', to='levelup_api.homework')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.level')),
                ('rate_class', models.ManyToManyField(related_name='rate_class', through='levelup_api.Rate_Class_Details', to='levelup_api.class')),
                ('rate_exercise', models.ManyToManyField(related_name='rate_exercise', through='levelup_api.Rate_Exercise_Details', to='levelup_api.speaking_exercise')),
                ('requested_class', models.ManyToManyField(db_table='levelup_api_request_class', to='levelup_api.class')),
                ('requested_exercise', models.ManyToManyField(through='levelup_api.Request_Exercise', to='levelup_api.language_native')),
            ],
        ),
        migrations.AddField(
            model_name='speaking_exercise',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.student'),
        ),
        migrations.AddField(
            model_name='request_exercise',
            name='language_native',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.language_native'),
        ),
        migrations.AddField(
            model_name='request_exercise',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.student'),
        ),
        migrations.AddField(
            model_name='rate_exercise_details',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.student'),
        ),
        migrations.AddField(
            model_name='rate_class_details',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.student'),
        ),
        migrations.CreateModel(
            name='Homework_Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_datetime', models.DateTimeField()),
                ('date', models.FileField(upload_to='')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.homework')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.student')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levelup_api.teacher'),
        ),
    ]
