from django.contrib import admin
from .models import Language_Native, System_User, User, Teacher, Student

admin.site.register(User)
admin.site.register(System_User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Language_Native)
