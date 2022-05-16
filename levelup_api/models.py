from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
User._meta.get_field('email').null = False


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)


class System_User(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    date_birth = models.DateField()
    photo = models.ImageField()


class System_Admin(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)


class Student(models.Model):
    system_user = models.OneToOneField(
        "levelup_api.System_User", on_delete=models.CASCADE, primary_key=True)
    contact_no = models.CharField(max_length=12)
    homeworks = models.ManyToManyField(
        "levelup_api.Homework", db_table="levelup_api_get_hw")
    classes = models.ManyToManyField(
        "levelup_api.Class", db_table="levelup_api_takes", related_name="classes")
    requested_exercise = models.ManyToManyField(
        "levelup_api.Language_Native", through="Request_Exercise")
    level = models.ForeignKey("levelup_api.Level", on_delete=models.CASCADE)
    requested_class = models.ManyToManyField(
        "levelup_api.Class", db_table="levelup_api_request_class")
    rate_class = models.ManyToManyField(
        "levelup_api.Class", through="levelup_api.Rate_Class_Details", related_name="rate_class")
    rate_exercise = models.ManyToManyField(
        "levelup_api.Speaking_Exercise", through="levelup_api.Rate_Exercise_Details", related_name="rate_exercise")


class Teacher(models.Model):
    system_user = models.OneToOneField(
        "levelup_api.System_User", on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    rating = models.FloatField()
    yearsOfExperience = models.IntegerField()
    languages = models.ManyToManyField(
        "levelup_api.Language", db_table="levelup_api_knows")


class Language_Native(models.Model):
    system_user = models.OneToOneField(
        "levelup_api.System_User", on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    rating = models.FloatField()
    speaks = models.ManyToManyField(
        "levelup_api.Language", null=False, db_table="levelup_api_speaks")


class Class(models.Model):
    capacity = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    weekly_plan = models.TextField()
    enrollment = models.IntegerField()
    language = models.ForeignKey(
        "levelup_api.Language", on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        "levelup_api.Teacher", on_delete=models.CASCADE)
    level = models.ForeignKey("levelup_api.Level", on_delete=models.CASCADE)
    image = models.ImageField()
    books = models.ManyToManyField(
        "levelup_api.Class_Book", db_table="levelup_api_require_books")


class Speaking_Exercise(models.Model):
    exercise_link = models.TextField()
    exercise_datetime = models.DateTimeField()
    grade = models.FloatField()
    student = models.ForeignKey(
        "levelup_api.Student", on_delete=models.CASCADE)
    language = models.ForeignKey(
        "levelup_api.Language", on_delete=models.CASCADE)
    language_native = models.ForeignKey(
        "levelup_api.Language_Native", on_delete=models.CASCADE)


class Class_Book(models.Model):
    book_name = models.TextField()


class Homework(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_datetime = models.DateTimeField()
    assign_datetime = models.DateTimeField()
    grade = models.FloatField()
    given_class = models.ForeignKey(
        "levelup_api.Class", on_delete=models.CASCADE)


class Language(models.Model):
    lang_name = models.CharField(max_length=80, null=False, unique=True)


class Forum_Topic(models.Model):
    datetime = models.DateTimeField()
    status = models.CharField(max_length=20)
    topic_title = models.TextField()
    topic_text = models.TextField()
    topic_owner = models.ForeignKey(
        "levelup_api.System_User", on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        "levelup_api.Tag", db_table="levelup_api_topic_tags")


class Forum_Reply_Comment(models.Model):
    datetime = models.DateTimeField()
    comment_text = models.TextField()
    comment_owner = models.ForeignKey(
        "levelup_api.System_User", on_delete=models.CASCADE)
    reply = models.ForeignKey(
        "levelup_api.Forum_Reply", on_delete=models.CASCADE)


class Request_Exercise(models.Model):
    student = models.ForeignKey(
        "levelup_api.Student", on_delete=models.CASCADE)
    language_native = models.ForeignKey(
        "levelup_api.Language_Native", on_delete=models.CASCADE)
    requested_datetime = models.DateTimeField()
    status = models.CharField(max_length=20)
    additional_notes = models.TextField()
    created_at = models.DateTimeField()


class Homework_Upload(models.Model):
    homework = models.ForeignKey(
        "levelup_api.Homework", on_delete=models.CASCADE)
    student = models.ForeignKey(
        "levelup_api.Student", on_delete=models.CASCADE)
    upload_datetime = models.DateTimeField()
    date = models.FileField()


class Level(models.Model):
    level_title = models.CharField(max_length=80, null=False, unique=True)


class Forum_Reply(models.Model):
    datetime = models.DateTimeField()
    reply_text = models.TextField()
    user = models.ForeignKey("levelup_api.System_User",
                             on_delete=models.CASCADE)
    topic = models.ForeignKey(
        "levelup_api.Forum_Topic", on_delete=models.CASCADE)


class Tag(models.Model):
    tag_title = models.CharField(max_length=100, null=False)


class Rate_Class_Details(models.Model):
    rate = models.FloatField()
    rate_datetime = models.DateTimeField()
    given_class = models.ForeignKey(
        "levelup_api.Class", on_delete=models.CASCADE)
    student = models.ForeignKey(
        "levelup_api.Student", on_delete=models.CASCADE)


class Rate_Exercise_Details(models.Model):
    rate = models.FloatField()
    review = models.TextField()
    rate_datetime = models.DateTimeField()
    speaking_exercise = models.ForeignKey(
        "levelup_api.Speaking_Exercise", on_delete=models.CASCADE)
    student = models.ForeignKey(
        "levelup_api.Student", on_delete=models.CASCADE)
