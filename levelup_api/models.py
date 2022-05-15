from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)


class SystemUser(models.Model):
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
    contactNo = models.CharField(max_length=12)
    # todo: add level


class Teacher(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    rating = models.FloatField()
    yearsOfExperience = models.IntegerField()


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
    teacher = models.OneToOneField("levelup_api.Teacher")
    # todo: level_id INT NOT NULL,
    image = models.ImageField()


class SpeakingExercise(models.Model):
    exerciseLink = models.TextField()
    exerciseDatetime = models.DateTimeField()
    grade = models.FloatField()
    student = models.OneToOneField("levelup.Student")
    # todo: lang_id INT NOT NULL,
    languageNative = models.OneToOneField("levelup.LanguageNative")


class ClassBook(models.Model):
    bookName = models.TextField()


class Homework(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    dueDatetime = models.DateTimeField()
    assignDatetime = models.DateTimeField()
    grade = models.FloatField()
    givenClass = models.OneToOneField("levelup.Class")
