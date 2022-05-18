from rest_framework import serializers


from .models import *


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
        res['comment_owner'] = UserSerializer(
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


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
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
        response['language_native'] = LanguageNativeSerializer(
            instance.language_native).data
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
        response['topic_owner'] = UserSerializer(
            instance.forum_topic).data
        response['tags'] = TagSerializer(instance.tags, many=True).data
        return response


class RequestExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request_Exercise
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['student'] = StudentSerializer(instance.student).data
        response['language_native'] = LanguageNativeSerializer(
            instance.language_native).data
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
        response['speaking_exercise'] = SpeakingExerciseSerializer(
            instance.speaking_exercise).data
        response['student'] = StudentSerializer(
            instance.student, many=True).data
        return response


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    is_system_admin = serializers.BooleanField(default=False)
    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)
    is_language_native = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'phone', 'is_system_admin',
                  'is_student', 'is_teacher', 'is_language_native', 'token']
        extra_kwargs = {
            'token': {
                'read_only': True
            },
        }


class SystemAdminSignupSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=60)
    username = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255, write_only=True)
    phone = serializers.CharField(max_length=20)
    is_active = serializers.BooleanField(default=True)
    is_staff = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(allow_null=True, default=None)
    updated_at = serializers.DateTimeField(allow_null=True, default=None)
    is_system_admin = serializers.BooleanField(default=False)
    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)
    is_language_native = serializers.BooleanField(default=False)
    date_birth = serializers.DateField(allow_null=True, default=None)

    class Meta:
        model = User
        fields = ['name', 'email', 'username',
                  'password', 'phone', 'date_birth']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            phone=self.validated_data['phone'],
            is_active=self.validated_data['is_active'],
            is_staff=self.validated_data['is_staff'],
            created_at=self.validated_data['created_at'],
            updated_at=self.validated_data['updated_at'],
            is_system_admin=True,
            date_birth=self.validated_data['date_birth'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        System_Admin.objects.create(user=user)
        return user


class StudentSignupSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=60)
    username = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255, write_only=True)
    phone = serializers.CharField(max_length=20)
    is_active = serializers.BooleanField(default=True)
    is_staff = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(allow_null=True, default=None)
    updated_at = serializers.DateTimeField(allow_null=True, default=None)
    is_system_admin = serializers.BooleanField(default=False)
    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)
    is_language_native = serializers.BooleanField(default=False)
    date_birth = serializers.DateField(allow_null=True, default=None)

    class Meta:
        model = User
        fields = ['name', 'email', 'username',
                  'password', 'phone', 'date_birth', 'level']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            phone=self.validated_data['phone'],
            is_active=self.validated_data['is_active'],
            is_staff=self.validated_data['is_staff'],
            created_at=self.validated_data['created_at'],
            updated_at=self.validated_data['updated_at'],
            is_student=True,
            date_birth=self.validated_data['date_birth'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        Student.objects.create(user=user)
        return user


class TeacherSignupSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=60)
    username = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255, write_only=True)
    phone = serializers.CharField(max_length=20)
    is_active = serializers.BooleanField(default=True)
    is_staff = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(allow_null=True, default=None)
    updated_at = serializers.DateTimeField(allow_null=True, default=None)
    is_system_admin = serializers.BooleanField(default=False)
    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)
    is_language_native = serializers.BooleanField(default=False)
    date_birth = serializers.DateField(allow_null=True, default=None)
    knows = LanguageSerializer(many=True)
    description = serializers.CharField(allow_null=True, default=None)
    years_of_experience = serializers.IntegerField(
        allow_null=True, default=None)

    class Meta:
        model = User
        fields = ['name', 'email', 'username',
                  'password', 'phone', 'date_birth',
                  'knows', 'description', 'years_of_experience']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            phone=self.validated_data['phone'],
            is_active=self.validated_data['is_active'],
            is_staff=self.validated_data['is_staff'],
            created_at=self.validated_data['created_at'],
            updated_at=self.validated_data['updated_at'],
            is_teacher=True,
            date_birth=self.validated_data['date_birth'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        teacher = Teacher(
            user=user,
            description=self.validated_data['description'],
            years_of_experience=self.validated_data['years_of_experience'],
        )
        teacher.save()
        for dictionary in self.validated_data['knows']:
            language = dictionary['lang_name']
            teacher.knows.add(Language.objects.get(lang_name=language))
        return user


class LanguageNativeSignupSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=60)
    username = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255, write_only=True)
    phone = serializers.CharField(max_length=20)
    is_active = serializers.BooleanField(default=True)
    is_staff = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(allow_null=True, default=None)
    updated_at = serializers.DateTimeField(allow_null=True, default=None)
    is_system_admin = serializers.BooleanField(default=False)
    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)
    is_language_native = serializers.BooleanField(default=False)
    date_birth = serializers.DateField(allow_null=True, default=None)
    speaks = LanguageSerializer(many=True)
    description = serializers.CharField(allow_null=True, default=None)

    class Meta:
        model = User
        fields = ['name', 'email', 'username',
                  'password', 'phone',
                  'date_birth', 'speaks', 'description']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            phone=self.validated_data['phone'],
            is_active=self.validated_data['is_active'],
            is_staff=self.validated_data['is_staff'],
            created_at=self.validated_data['created_at'],
            updated_at=self.validated_data['updated_at'],
            is_language_native=True,
            date_birth=self.validated_data['date_birth'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        languageNative = Language_Native(
            user=user,
            description=self.validated_data['description']
        )
        languageNative.save()
        for dictionary in self.validated_data['speaks']:
            language = dictionary['lang_name']
            languageNative.speaks.add(
                Language.objects.get(lang_name=language))
        return user
