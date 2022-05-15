from winreg import DisableReflectionKey
from rest_framework import serializers

from .models import *
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
        
        
