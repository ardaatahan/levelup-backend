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
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['student'] = StudentSerializer(instance.student).data
        response['language'] = LanguageSerializer(instance.language).data
        response['language_native'] = LanguageNativeSerializer(instance.language_native).data
        return response


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = "__all__"
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['given_class'] = ClassSerializer(instance.given_class).data
        return response 


class ForumTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum_Topic
        fields = "__all__"
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['topic_owner'] = SystemUserSerializer(instance.forum_topic).data
        response['tags'] = TagSerializer(instance.tags, many=True).data
        return response 


class RequestExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request_Exercise
        fields = "__all__"
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['student'] = StudentSerializer(instance.student).data
        response['language_native'] = LanguageNativeSerializer(instance.language_native, many=True).data
        return response


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
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['speaking_exercise'] = SpeakingExerciseSerializer(instance.speaking_exercise).data
        response['student'] = StudentSerializer(instance.student, many=True).data
        return response
