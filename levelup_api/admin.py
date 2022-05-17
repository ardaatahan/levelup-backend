from urllib.request import Request
from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Language_Native)
admin.site.register(Language)
admin.site.register(Level)
admin.site.register(Class)
admin.site.register(Speaking_Exercise)
admin.site.register(Class_Book)
admin.site.register(Homework)
admin.site.register(Forum_Topic)
admin.site.register(Forum_Reply_Comment)
admin.site.register(Request_Exercise)
admin.site.register(Homework_Upload)
admin.site.register(Forum_Reply)
admin.site.register(Tag)
admin.site.register(Rate_Class_Details)
admin.site.register(Rate_Exercise_Details)
