from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, name, username, email, phone, password=None):
        if not name:
            raise TypeError('Users must have a name')
        if not username:
            raise TypeError('Users must have a username')
        if not email:
            raise TypeError('Users must have an email address')
        user = self.model(name=name, username=username,
                          email=self.normalize_email(email), phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, username, email, phone, password):
        if not password:
            raise TypeError('Superusers must have a password')
        user = self.create_user(name, username, email, phone, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=60, null=False,
                             unique=True, db_index=True)
    password = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=20)
    username = models.CharField(
        max_length=50, null=False, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_system_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_language_native = models.BooleanField(default=False)
    date_birth = models.DateField(null=True)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = UserManager()


class System_Admin(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)


class Student(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    contact_no = models.CharField(max_length=12, null=True, blank=True)
    homeworks = models.ManyToManyField(
        "levelup_api.Homework", db_table="levelup_api_get_hw", null=True, blank=True)
    classes = models.ManyToManyField(
        "levelup_api.Class", db_table="levelup_api_takes", related_name="classes", null=True, blank=True)
    requested_exercise = models.ManyToManyField(
        "levelup_api.Language_Native", through="Request_Exercise", null=True, blank=True)
    requested_class = models.ManyToManyField(
        "levelup_api.Class", db_table="levelup_api_request_class", null=True, blank=True)
    rate_class = models.ManyToManyField(
        "levelup_api.Class", through="levelup_api.Rate_Class_Details", related_name="rate_class", null=True, blank=True)
    rate_exercise = models.ManyToManyField(
        "levelup_api.Speaking_Exercise", through="levelup_api.Rate_Exercise_Details", related_name="rate_exercise", null=True, blank=True)


class Teacher(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    knows = models.ManyToManyField(
        "levelup_api.Language", db_table="levelup_api_knows", null=True, blank=True, related_name="knows")


class Language_Native(models.Model):
    user = models.OneToOneField(
        "levelup_api.User", on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    speaks = models.ManyToManyField(
        "levelup_api.Language", db_table="levelup_api_speaks", null=True, blank=True, related_name="speaks")


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
    lang_name = models.CharField(max_length=80, null=False)


class Forum_Topic(models.Model):
    datetime = models.DateTimeField()
    status = models.CharField(max_length=20)
    topic_title = models.TextField()
    topic_text = models.TextField()
    topic_owner = models.ForeignKey(
        "levelup_api.User", on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        "levelup_api.Tag", db_table="levelup_api_topic_tags")


class Forum_Reply_Comment(models.Model):
    datetime = models.DateTimeField()
    comment_text = models.TextField()
    comment_owner = models.ForeignKey(
        "levelup_api.User", on_delete=models.CASCADE)
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
    level_title = models.CharField(max_length=80, null=False)


class Forum_Reply(models.Model):
    datetime = models.DateTimeField()
    reply_text = models.TextField()
    reply_owner = models.ForeignKey("levelup_api.User",
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
