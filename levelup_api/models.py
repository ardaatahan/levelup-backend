from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)


class SystemUser(models.Model):
    user = models.OneToOneField("levelup_api.User", on_delete=models.CASCADE)
    dateBirth = models.DateField()
    photo = models.ImageField()


class SystemAdmin(models.Model):
    user = models.OneToOneField("levelup_api.User", on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField("levelup_api.User", on_delete=models.CASCADE)
    contactNo = models.CharField(max_length=12)
    # add level


class Teacher(models.Model):
    user = models.OneToOneField("levelup_api.User", on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.DecimalField()
    yearsOfExperience = models.IntegerField()
