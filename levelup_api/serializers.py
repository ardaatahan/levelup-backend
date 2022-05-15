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


class SystemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = System_User
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class LanguageNativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language_Native
        fields = "__all__"


class SpeakingExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaking_Exercise
        fields = "__all__"


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = "__all__"


class ForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum_Topic
        fields = "__all__"


class RequestExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request_Exercise
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class RateExerciseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate_Exercise_Details
        fields = "__all__"
