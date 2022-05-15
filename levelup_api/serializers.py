from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class SystemAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = System_Admin
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"


class ClassBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class_Book
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class ForumReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum_Reply_Comment
        fields = "__all__"


class HomeworkUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework_Upload
        fields = "__all__"


class ForumReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum_Reply
        fields = "__all__"


class RateClassDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate_Class_Details
        fields = "__all__"
