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
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    contact_no = models.CharField(max_length=12)
    level = models.ForeignKey("levelup_api.Level", on_delete=models.CASCADE)
    requested_class = models.ManyToManyField(
        "levelup_api.Class", db_table="levelup_api_request_class")
    rate_class = models.ManyToManyField(
        "levelup_api.Class", through="levelup_api.Rate_Class_Details")
    rate_exercise = models.ManyToManyField(
        "levelup_api.Speaking_Exercise", through="levelup_api.Rate_Exercise_Details")


class Teacher(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    rating = models.FloatField()
    years_of_experience = models.IntegerField()


class Language_Native(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    rating = models.FloatField()
    speaks = models.ManyToManyField(
        "levelup_api.Language", on_delete=models.CASCADE, null=False, db_table="levelup_api_speaks")


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
