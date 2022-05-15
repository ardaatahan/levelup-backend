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

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['language'] = LanguageSerializer(instance.language).data
        res['teacher'] = TeacherSerializer(instance.teacher).data
        res['level'] = LevelSerializer(instance.level).data
        res['books'] = ClassBookSerializer(instance.books, many=True).data
        return res


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

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['comment_owner'] = SystemUserSerializer(
            instance.comment_owner).data
        res['reply'] = ForumReplySerializer(instance.reply).data
        return res


class HomeworkUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework_Upload
        fields = "__all__"

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['homework'] = HomeworkSerializer(
            instance.homework).data
        res['student'] = StudentSerializer(instance.reply).data
        return res


class ForumReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum_Reply
        fields = "__all__"

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['user'] = UserSerializer(instance.user).data
        res['topic'] = ForumTopicSerializer(instance.topic).data
        return res


class RateClassDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate_Class_Details
        fields = "__all__"

    def to_representation(self, instance):
        res = super.to_representation(instance)
        res['given_class'] = ClassSerializer(instance).data
        res['student'] = StudentSerializer(instance).data
        return res


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
