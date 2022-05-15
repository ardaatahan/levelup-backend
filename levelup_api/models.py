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
    dateBirth = models.DateField()
    photo = models.ImageField()


class SystemAdmin(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)


class Student(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    contact_no = models.CharField(max_length=12)
    # todo: add level
    homeworks = models.ManyToManyField(
        "levelup_api.Homework", db_table="levelup_api_get_hw")
    classes = models.ManyToManyField(
        "levelup_api.Class", db_table="levelup_api_takes")
    requested_exercise = models.ManyToManyField("levelup_api.Language_Native", through="Request_Exercise")
    

class Teacher(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    rating = models.FloatField()
    yearsOfExperience = models.IntegerField()
    languages = models.ManyToManyField(
        "levelup_api.Language", db_table="levelup_api_knows")


class LanguageNative(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    rating = models.FloatField()


class Class(models.Model):
    capacity = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    startDate = models.DateField()
    endDate = models.DateField()
    weeklyPlan = models.TextField()
    enrollment = models.IntegerField()
    # todo: lang_id INT NOT NULL,
    teacher = models.ForeignKey(
        "levelup_api.Teacher", on_delete=models.CASCADE)
    # todo: level_id INT NOT NULL,
    image = models.ImageField()
    books = models.ManyToManyField(
        "levelup_api.Class_Book", db_table="levelup_api_require_books")


class Speaking_Exercise(models.Model):
    exerciseLink = models.TextField()
    exerciseDatetime = models.DateTimeField()
    grade = models.FloatField()
    student = models.ForeignKey(
        "levelup_api.Student", on_delete=models.CASCADE)
    # todo: lang_id INT NOT NULL,clear
    languageNative = models.ForeignKey(
        "levelup_api.Language_Native", on_delete=models.CASCADE)


class ClassBook(models.Model):
    bookName = models.TextField()


class Homework(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    dueDatetime = models.DateTimeField()
    assignDatetime = models.DateTimeField()
    grade = models.FloatField()
    givenClass = models.OneToOneField(
        "levelup_api.Class", on_delete=models.CASCADE)


class Language(models.Model):
    lang_name = models.CharField(max_length=80, null=False, unique=True)
    
class Forum_Topic(models.Model):
    datetime = models.DateTimeField()
    status = models.CharField(max_length=20)
    topic_title = models.TextField()
    topic_text = models.TextField()
    topic_owner = models.ForeignKey("levelup_api.System_User", on_delete=models.CASCADE)
    
class Forum_Reply_Comment(models.Model):
    datetime = models.DateTimeField()
    comment_text = models.TextField()
    comment_owner = models.ForeignKey("levelup_api_System_User", on_delete=models.CASCADE)
    reply_owner = models.ForeignKey("levelup_api.Forum_Reply", on_delete=models.CASCADE)
    
class Request_Exercise(models.Model):
    student = models.ForeignKey("levelup_api.Student", on_delete=models.CASCADE)
    language_native = models.ForeignKey("levelup_api.Language_Native", on_delete=models.CASCADE)
    requested_datetime = models.DateTimeField()
    status = models.CharField(max_length=20)
    additional_notes = models.TextField()
    created_at = models.DateTimeField()