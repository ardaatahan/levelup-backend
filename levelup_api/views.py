from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.db import connection
import json

from .models import *
from .serializers import *
from .permissions import *


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class LogoutAPIView(APIView):
    def post(self, req, format=None):
        req.auth.delete()
        return Response(status=status.HTTP_200_OK)


class SystemAdminOnlyView(RetrieveAPIView):
    permission_classes = [IsAuthenticated & IsSystemAdminUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class StudentOnlyView(RetrieveAPIView):
    permission_classes = [IsAuthenticated & IsStudentUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class TeacherOnlyView(RetrieveAPIView):
    permission_classes = [IsAuthenticated & IsTeacherUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LanguageNativeOnlyView(RetrieveAPIView):
    permission_classes = [IsAuthenticated & IsLanguageNativeUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CustomAuthToken(ObtainAuthToken):
    def post(self, req):
        serializer = self.serializer_class(
            data=req.data, context={'request': req})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_system_admin': user.is_system_admin,
            'is_student': user.is_student,
            'is_teacher': user.is_teacher,
            'is_language_native': user.is_language_native,
        })


class SystemAdminSignupAPIView(GenericAPIView):
    serializer_class = SystemAdminSignupSerializer

    def post(self, req):
        serializer = SystemAdminSignupSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "System Admin account has been created successfully"
        })


class StudentSignupAPIView(GenericAPIView):
    serializer_class = StudentSignupSerializer

    def post(self, req):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "Student account has been created successfully"
        })


class TeacherSignupAPIView(GenericAPIView):
    serializer_class = TeacherSignupSerializer

    def post(self, req):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "Teacher account has been created successfully"
        })


class LanguageNativeSignupAPIView(GenericAPIView):
    serializer_class = LanguageNativeSignupSerializer

    def post(self, req):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "Language Native account has been created successfully"
        })


class SpeakingExerciseListView(APIView):
    def get(self, req, *args, **kwargs):
        #speaking_exercises = Speaking_Exercise.objects.all()
        speaking_exercises = Speaking_Exercise.objects.raw(
            'SELECT * FROM levelup_api_speaking_exercise')
        serializer = SpeakingExerciseSerializer(speaking_exercises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, *args, **kwargs):
        serializer = SpeakingExerciseSerializer(data=req.data)
        if serializer.is_valid():
            #cursor = connection.cursor()
            #cursor.execute("INSERT INTO levelup_api_speaking_exercise(exercise_link, exercise_datetime, grade, language_id, language_native_id, student_id) VALUES (%s, %s, %f, %d, %d, %d)", [serializer.validated_data['level_title']])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Lists native speakers according to language and level selected
class FindNativeSpeakerListAPIView(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''WITH native_rating(language_native_id, avg_rating) AS
        (
            SELECT Sp.language_native_id, AVG(R.rate)
            FROM levelup_api_rate_exercise_details R, levelup_api_speaking_exercise Sp
            WHERE R.speaking_exercise_id = Sp.id
            GROUP BY Sp.language_native_id
        )
        SELECT U.name, N.avg_rating FROM levelup_api_user U, native_rating N WHERE N.language_native_id = U.id'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        native_speakers = cursor.fetchall()
        # rs is a list of tuples, json.dumps converts it to json object
        rs = json.dumps(dict(native_speakers))
        return Response(rs, status=status.HTTP_200_OK)


class SpeakingExerciseAPIView(APIView):
    def getExerciseObject(self, exercise_id):
        try:
            # return Speaking_Exercise.objects.get(id=exercise_id)
            return Speaking_Exercise.objects.raw('SELECT * FROM levelup_api_speaking_exercise WHERE id = %s', [exercise_id])[0]
        except:
            return None

    def get(self, req, exercise_id, *args, **kwargs):
        exerciseObject = self.getExerciseObject(exercise_id)
        if not exerciseObject:
            return Response(
                {"res": f"Speaking Exercise with id {exercise_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SpeakingExerciseSerializer(exerciseObject)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, exercise_id, *args, **kwargs):
        exerciseObject = self.getExerciseObject(exercise_id)
        if not exerciseObject:
            return Response(
                {"res": f"Speaking Exercise with id {exercise_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SpeakingExerciseSerializer(
            instance=exerciseObject, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, exercise_id, *args, **kwargs):
        exerciseObject = self.getExerciseObject(exercise_id)
        if not exerciseObject:
            return Response(
                {"res": f"Object with Speaking Exercise id {exercise_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # exerciseObject.delete()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM levelup_api_speaking_exercise WHERE id= %s", [exercise_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

# Returns all speaking exercises info for a language native


class SpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.name, Sp.exercise_datetime, Sp.exercise_link FROM levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U WHERE Sp.language_native_id = %s AND Sp.student_id = U.id'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = cursor.fetchall()
        # rs is a list of tuples, json.dumps converts it to json object
        rs = json.dumps(dict(speaking_exercises))
        return Response(rs, status=status.HTTP_200_OK)

# Returns only ungraded speaking exercises info for a language native


class UngradedSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.id, U.name, Sp.exercise_datetime, Sp.exercise_link, Sp.grade FROM levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U WHERE Sp.language_native_id = %s AND Sp.student_id = U.id AND Sp.grade IS NULL'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = dictfetchall(cursor)
        rs = json.dumps(speaking_exercises, default=str)
        return Response(rs, status=status.HTTP_200_OK)

# Returns only graded speaking exercises info for a language native


class GradedSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.id, U.name, Sp.exercise_datetime, Sp.exercise_link, Sp.grade FROM levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U WHERE Sp.language_native_id = %s AND Sp.student_id = U.id AND Sp.grade IS NOT NULL'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = dictfetchall(cursor)
        rs = json.dumps(speaking_exercises, default=str)
        return Response(rs, status=status.HTTP_200_OK)

# Returns only upcoming speaking exercises info for a language native


class UpcomingSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.id, U.name, Sp.exercise_datetime, Sp.exercise_link, Sp.grade FROM levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U WHERE Sp.language_native_id = %s AND Sp.student_id = U.id AND Sp.exercise_datetime > NOW()'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = dictfetchall(cursor)
        rs = json.dumps(speaking_exercises, default=str)
        return Response(rs, status=status.HTTP_200_OK)

# Returns only past speaking exercises info for a language native


class PastSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.id, U.name, Sp.exercise_datetime, Sp.exercise_link, Sp.grade FROM levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U WHERE Sp.language_native_id = %s AND Sp.student_id = U.id AND Sp.exercise_datetime < NOW()'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = dictfetchall(cursor)
        rs = json.dumps(speaking_exercises, default=str)
        return Response(rs, status=status.HTTP_200_OK)

# Returns only pending speaking exercise requests info for a language native


class RequestedSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.id, U.name, R.requested_datetime, R.additional_notes FROM levelup_api_request_exercise R,
        levelup_api_user U WHERE R.language_native_id = %s AND R.student_id = U.id AND R.status IS NULL'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        requests = dictfetchall(cursor)
        rs = json.dumps(requests, default=str)
        return Response(rs, status=status.HTTP_200_OK)

# Returns only declined speaking exercise requests info for a language native


class DeclinedRequestedSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.id, U.name, R.requested_datetime, R.additional_notes FROM levelup_api_request_exercise R,
        levelup_api_user U WHERE R.language_native_id = %s AND R.student_id = U.id AND R.status=%s'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id, 'DECLINED'])
        requests = dictfetchall(cursor)
        rs = json.dumps(requests, default=str)
        return Response(rs, status=status.HTTP_200_OK)

# Returns only accepted speaking exercise requests info for a language native


class AcceptedRequestedSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.id, U.name, R.requested_datetime, R.additional_notes FROM levelup_api_request_exercise R,
        levelup_api_user U WHERE R.language_native_id = %s AND R.student_id = U.id AND R.status=%s'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id, 'ACCEPTED'])
        requests = dictfetchall(cursor)
        rs = json.dumps(requests, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class SpeakingExercisesListAPIViewForStudent(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.name, Sp.exercise_datetime, Sp.exercise_link, Sp.grade, R.rate 
FROM levelup_api_speaking_exercise as Sp, levelup_api_user as U, levelup_api_rate_exercise_details as R
WHERE Sp.student_id = %s AND Sp.language_native_id = U.id AND R.speaking_exercise_id = Sp.id'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = dictfetchall(cursor)
        # rs is a list of tuples, json.dumps converts it to json object
        rs = json.dumps(speaking_exercises, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class UpcomingSpeakingExercisesListAPIViewForStudent(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT R.id, U.name, Sp.exercise_datetime, Sp.exercise_link, Sp.grade, R.rate FROM levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U, levelup_api_rate_exercise_details R
        WHERE Sp.student_id = %s AND Sp.language_native_id = U.id AND R.speaking_exercise_id = Sp.id AND Sp.exercise_datetime > NOW()'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = dictfetchall(cursor)
        rs = json.dumps(speaking_exercises, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class RequestedSpeakingExercisesListAPIViewForStudent(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT R.id, U.name, R.requested_datetime, R.additional_notes FROM levelup_api_request_exercise R,
        levelup_api_user U WHERE R.student_id = %s AND U.id = R.language_native_id'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        requests = dictfetchall(cursor)
        rs = json.dumps(requests, default=str)
        return Response(rs, status=status.HTTP_200_OK)

# Lists language natives according to language and level selected


class LanguageNativeListAPIView(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''WITH native_rating(language_native_id, avg_rating) AS
        (
            SELECT Sp.language_native_id, AVG(R.rate)
            FROM levelup_api_rate_exercise_details R, levelup_api_speaking_exercise Sp
            WHERE R.speaking_exercise_id = Sp.id
            GROUP BY Sp.language_native_id
        )
        SELECT U.id, U.name, N.avg_rating FROM levelup_api_user U, levelup_api_speaks S, levelup_api_language La
        native_rating N WHERE N.language_native_id = S.language_native_id AND La.id = S.language_id AND U.id = S.language_native_id AND La.lang_name = %s'''
        cursor = connection.cursor()
        # query parameters .../?lang="english"..
        cursor.execute(sql, [self.request.GET.get('lang')])
        classes = cursor.fetchall()
        rs = json.dumps(dict(classes))
        return Response(rs, status=status.HTTP_200_OK)

# Post: Requests an exercise
# Get: Gets specific language native


class RequestSpeakingExerciseAPIView(APIView):
    def get(self, req, native_id, *args, **kwargs):
        sql = '''WITH native_rating(language_native_id, avg_rating) AS
            (
                SELECT Sp.language_native_id, AVG(R.rate)
                FROM levelup_api_rate_exercise_details R, levelup_api_speaking_exercise Sp
                WHERE R.speaking_exercise_id = Sp.id
                GROUP BY Sp.language_native_id
            )
            SELECT U.name, N.avg_rating, L.description FROM levelup_api_user U, native_rating N, levelup_api_language_native L
            WHERE L.user_id = %s AND U.id = L.user_id AND native_rating.language_native_id = U.id'''
        cursor = connection.cursor()
        cursor.execute(sql, [native_id])
        classes = cursor.fetchall()
        rs = json.dumps(dict(classes))
        return Response(rs, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = RequestExerciseSerializer(data=req.data)
        if serializer.is_valid():
            cursor = connection.cursor()
            sql = '''INSERT INTO levelup_api_request_exercise(requested_datetime, additional_notes, language_native_id, student_id) 
            VALUES(%s, %s, %s, %s)'''
            cursor.execute(sql, [serializer.validated_data['requested_datetime'], serializer.validated_data['additional_notes'],
                                 serializer.validated_data['language_native_id'], req.user.id])
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeworkGradesListAPIViewForStudent(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT DISTINCT(H.id), H.name, C.title, H.assign_datetime, H.due_datetime, H.grade FROM levelup_api_user U, 
        levelup_api_class C, levelup_api_homework H, levelup_api_get_hw GH
        WHERE GH.student_id = %s AND H.given_class_id = C.id AND H.id = GH.homework_id'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        homeworks = dictfetchall(cursor)
        rs = json.dumps(homeworks, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class ExerciseGradesListAPIViewForStudent(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT DISTINCT(Sp.id), U.name, Sp.exercise_datetime, Sp.grade FROM levelup_api_user U, 
        levelup_api_speaking_exercise Sp
        WHERE Sp.student_id = %s AND U.id = Sp.language_native_id'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        exercises = dictfetchall(cursor)
        rs = json.dumps(exercises, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class ClassesListAPIViewForTeacher(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT C.id, C.title, La.lang_name, Le.level_title, C.start_date, C.end_date, C.capacity, C.enrollment 
        FROM levelup_api_class C, levelup_api_language La, levelup_api_level Le 
        WHERE C.teacher_id = %s AND La.id = C.language_id AND Le.id = C.level_id'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        classes = dictfetchall(cursor)
        rs = json.dumps(classes, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class ClassRequestsListAPIViewForTeacher(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT RC.id, C.title, C.capacity, C.enrollment 
        FROM levelup_api_request_class RC, levelup_api_user U, levelup_api_class C
        WHERE C.teacher_id = %s AND RC.class_id = C.id AND RC.student_id = U.id'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        classes = dictfetchall(cursor)
        rs = json.dumps(classes, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class HomeworksListAPIViewForTeacher(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT H.id, H.name, C.title, H.due_datetime, H.description
        FROM levelup_api_homework H, levelup_api_class C
        WHERE H.given_class_id = C.id AND C.teacher_id = %s'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        homework = dictfetchall(cursor)
        rs = json.dumps(homework, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class HomeworkListView(APIView):
    def get(self, req, *args, **kwargs):
       # homeworks = Homework.objects.all()
        homeworks = Homework.objects.raw('SELECT * FROM levelup_api_homework')
        serializer = HomeworkSerializer(homeworks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, *args, **kwargs):
        serializer = HomeworkSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeworkAPIView(APIView):
    def getHomeworkObject(self, homework_id):
        try:
            # return Homework.objects.get(id=homework_id)
            return Homework.objects.raw('SELECT * FROM levelup_api_homework WHERE id = %s', [homework_id])[0]
        except:
            return None

    def get(self, req, homework_id, *args, **kwargs):
        homeworkObject = self.getHomeworkObject(homework_id)
        if not homeworkObject:
            return Response(
                {"res": f"Homework with id {homework_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = HomeworkSerializer(homeworkObject)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, homework_id, *args, **kwargs):
        homeworkObject = self.getHomeworkObject(homework_id)
        if not homeworkObject:
            return Response(
                {"res": f"Homework with id {homework_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = HomeworkSerializer(
            instance=homeworkObject, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, homework_id, *args, **kwargs):
        homeworkObject = self.getHomeworkObject(homework_id)
        if not homeworkObject:
            return Response(
                {"res": f"Object with Homework id {homework_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # homeworkObject.delete()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM levelup_api_homework WHERE id= %s", [homework_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class ForumTopicListView(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT FT.id, FT.topic_title, U.name, FT.datetime FROM levelup_api_forum_topic FT, levelup_api_user U WHERE U.id = FT.topic_owner_id'''
        cursor = connection.cursor()
        cursor.execute(sql, [])
        posts = dictfetchall(cursor)
        rs = json.dumps(posts, default=str)
        return Response(rs, status=status.HTTP_200_OK)

    # def get(self, req, *args, **kwargs):
        #topics = Forum_Topic.objects.all()
        #topics = Forum_Topic.objects.raw('SELECT * FROM levelup_api_forum_topic')
        #serializer = ForumTopicSerializer(topics, many=True)

        # return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, *args, **kwargs):
        serializer = ForumTopicSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterForumTopicListAPIView(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT FT.id, FT.topic_title, U.name, FT.datetime FROM 
        levelup_api_forum_topic FT, levelup_api_user U WHERE U.id = FT.topic_owner_id AND FT.topic_title LIKE \'%%s%%\''''
        cursor = connection.cursor()
        # query parameters .../?filter="Ho"..
        cursor.execute(sql, [self.request.GET.get('filter')])
        posts = dictfetchall(cursor)
        rs = json.dumps(posts, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class ForumTopicAPIView(APIView):
    def getForumTopicObject(self, topic_id):
        try:
            return Forum_Topic.objects.raw('SELECT * FROM levelup_api_forum_topic WHERE id = %s', [topic_id])[0]
        except:
            return None

    def get(self, req, topic_id, *args, **kwargs):
        forumTopicObject = self.getForumTopicObject(topic_id)
        if not forumTopicObject:
            return Response(
                {"res": f"Forum Topic with id {topic_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ForumTopicSerializer(forumTopicObject)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, topic_id, *args, **kwargs):
        forumTopicObject = self.getForumTopicObject(topic_id)
        if not forumTopicObject:
            return Response(
                {"res": f"Forum Topic with id {topic_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ForumTopicSerializer(
            instance=forumTopicObject, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, topic_id, *args, **kwargs):
        forumTopicObject = self.getForumTopicObject(topic_id)
        if not forumTopicObject:
            return Response(
                {"res": f"Object with Forum Topic id {topic_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # forumTopicObject.delete()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM levelup_api_forum_topic WHERE id= %s", [topic_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class RequestExerciseListView(APIView):
    def get(self, req, *args, **kwargs):
        #requests = Request_Exercise.objects.all()
        requests = Request_Exercise.objects.raw(
            'SELECT * FROM levelup_api_request_exercise')
        serializer = RequestExerciseSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, *args, **kwargs):
        serializer = RequestExerciseSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestExerciseAPIView(APIView):
    def getRequestObject(self, request_id):
        try:
            # return Request_Exercise.objects.get(id=request_id)
            return Request_Exercise.objects.raw('SELECT * FROM levelup_api_request_exercise WHERE id = %s', [request_id])[0]
        except:
            return None

    def get(self, req, request_id, *args, **kwargs):
        requestObject = self.getRequestObject(request_id)
        if not requestObject:
            return Response(
                {"res": f"Request Exercise with id {request_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RequestExerciseSerializer(requestObject)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, request_id, *args, **kwargs):
        requestObject = self.getRequestObject(request_id)
        if not requestObject:
            return Response(
                {"res": f"Request Exercise with id {request_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RequestExerciseSerializer(
            instance=requestObject, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, request_id, *args, **kwargs):
        requestObject = self.getRequestObject(request_id)
        if not requestObject:
            return Response(
                {"res": f"Object with Request Exercise id {request_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # requestObject.delete()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM levelup_api_request_exercise WHERE id= %s", [request_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class AdminReportNumOfStudentsAPIView(APIView):
    def get(self, req, *args, **kwargs):
        lang = self.request.GET.get('lang')
        level = self.request.GET.get('level')
        sql = '''SELECT COUNT(DISTINCT S.user_id) FROM levelup_api_student S WHERE 
        S.user_id IN (SELECT S2.user_id FROM levelup_api_student S2, levelup_api_class C, 
        levelup_api_takes T WHERE T.student_id = S2.user_id AND C.language_id = %s) OR S.user_id IN 
        (SELECT S3.user_id FROM levelup_api_student S3, levelup_api_speaking_exercise Sp WHERE S3.user_id = Sp.student_id AND
        Sp.language_id = %s)'''
        cursor = connection.cursor()
        # query parameters .../?lang="English"..
        cursor.execute(sql, [lang, lang])
        report = dictfetchall(cursor)
        rs = json.dumps(report, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class AdminReportExerciseAveragesAPIView(APIView):
    def get(self, req, *args, **kwargs):
        lang = self.request.GET.get('lang')
        sql = '''SELECT AVG(Sp.grade) FROM levelup_api_speaking_exercise Sp
        WHERE Sp.language_id = %s AND Sp.grade IS NOT NULL'''
        cursor = connection.cursor()
        cursor.execute(sql, [lang])  # query parameters .../?lang="English"..
        report = dictfetchall(cursor)
        rs = json.dumps(report, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class AdminReportHomeworkAveragesAPIView(APIView):
    def get(self, req, *args, **kwargs):
        lang = self.request.GET.get('lang')
        level = self.request.GET.get('level')
        sql = '''SELECT AVG(H.grade) FROM levelup_api_student S, levelup_api_homework H
        WHERE H.given_class_id IN (SELECT C.id FROM levelup_api_class C WHERE C.level_id = %s AND C.language_id = %s)
        AND H.grade IS NOT NULL'''
        cursor = connection.cursor()
        # query parameters .../?lang="English"..
        cursor.execute(sql, [level, lang])
        report = dictfetchall(cursor)
        rs = json.dumps(report, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class LevelListView(APIView):
    def get(self, req, *args, **kwargs):
        #levels = Level.objects.all()
        levels = Level.objects.raw('SELECT * FROM levelup_api_level')
        print(levels.query)
        serializer = LevelSerializer(levels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, *args, **kwargs):
        serializer = LevelSerializer(data=req.data)

        if serializer.is_valid():
            print(serializer.validated_data)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO levelup_api_level(level_title) VALUES (%s)", [
                           serializer.validated_data['level_title']])
            # serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LevelAPIView(APIView):
    def getLevelObject(self, level_id):
        try:
            # return Level.objects.get(id=level_id)
            return Level.objects.raw('SELECT * FROM levelup_api_level WHERE id = %s', [level_id])[0]
        except:
            return None

    def get(self, req, level_id, *args, **kwargs):
        levelObject = self.getLevelObject(level_id)
        if not levelObject:
            return Response(
                {"res": f"Level with id {level_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LevelSerializer(levelObject)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, level_id, *args, **kwargs):
        levelObject = self.getLevelObject(level_id)
        if not levelObject:
            return Response(
                {"res": f"Level with id {level_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LevelSerializer(
            instance=levelObject, data=req.data, partial=True)
        if serializer.is_valid():
            cursor = connection.cursor()
            cursor.execute("UPDATE levelup_api_level SET level_title = %s WHERE id= %s", [
                           serializer.validated_data['level_title'], level_id])
            # serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, level_id, *args, **kwargs):
        levelObject = self.getLevelObject(level_id)
        if not levelObject:
            return Response(
                {"res": f"Object with Level id {level_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        #res = levelObject.delete()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM levelup_api_level WHERE id= %s", [level_id])
        # print(res)
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class TagListView(APIView):
    def get(self, req, *args, **kwargs):
        #tags = Tag.objects.all()
        tags = Tag.objects.raw('SELECT * FROM levelup_api_tag')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, *args, **kwargs):
        serializer = TagSerializer(data=req.data)
        if serializer.is_valid():
            cursor = connection.cursor()
            cursor.execute("INSERT INTO levelup_api_tag(tag_title) VALUES (%s)", [
                           serializer.validated_data['tag_title']])
            # serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagAPIView(APIView):
    def getTagObject(self, tag_id):
        try:
            # return Tag.objects.get(id=tag_id)
            return Tag.objects.raw('SELECT * FROM levelup_api_tag WHERE id = %s', [tag_id])[0]
        except:
            return None

    def get(self, req, tag_id, *args, **kwargs):
        tagObject = self.getTagObject(tag_id)
        if not tagObject:
            return Response(
                {"res": f"Tag with id {tag_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TagSerializer(tagObject)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, tag_id, *args, **kwargs):
        tagObject = self.getTagObject(tag_id)
        if not tagObject:
            return Response(
                {"res": f"Tag with id {tag_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TagSerializer(
            instance=tagObject, data=req.data, partial=True)
        if serializer.is_valid():
            cursor = connection.cursor()
            cursor.execute("UPDATE levelup_api_tag SET tag_title = %s WHERE id= %s", [
                           serializer.validated_data['tag_title'], tag_id])
            # serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, tag_id, *args, **kwargs):
        tagObject = self.getTagObject(tag_id)
        if not tagObject:
            return Response(
                {"res": f"Object with Tag id {tag_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # tagObject.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_tag WHERE id= %s", [tag_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class RateExerciseDetailsListView(APIView):
    def get(self, req, *args, **kwargs):
        #rateExerciseDetails = Rate_Exercise_Details.objects.all()
        rateExerciseDetails = Rate_Exercise_Details.objects.raw(
            'SELECT * FROM levelup_api_rate_exercise_details')
        serializer = RateExerciseDetailsSerializer(
            rateExerciseDetails, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, *args, **kwargs):
        serializer = RateExerciseDetailsSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RateExerciseDetailsAPIView(APIView):
    def getDetailObject(self, detail_id):
        try:
            # return Rate_Exercise_Details.objects.get(id=detail_id)
            return Rate_Exercise_Details.objects.raw('SELECT * FROM levelup_api_rate_exercise_details WHERE id = %s', [detail_id])[0]
        except:
            return None

    def get(self, req, detail_id, *args, **kwargs):
        exerciseDetailObject = self.getDetailObject(detail_id)
        if not exerciseDetailObject:
            return Response(
                {"res": f"Rate Exercise Detail with id {detail_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RateExerciseDetailsSerializer(exerciseDetailObject)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, detail_id, *args, **kwargs):
        exerciseDetailObject = self.getDetailObject(detail_id)
        if not exerciseDetailObject:
            return Response(
                {"res": f"Detail with id {detail_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RateExerciseDetailsSerializer(
            instance=exerciseDetailObject, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, detail_id, *args, **kwargs):
        exerciseDetailObject = self.getTagObject(detail_id)
        if not exerciseDetailObject:
            return Response(
                {"res": f"Object with Rate Exercise Detail id {detail_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # exerciseDetailObject.delete()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM levelup_api_rate_exercise_details WHERE id= %s", [detail_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

# List Classes of a User


class ClassesOfStudentListAPIView(APIView):
    def get(self, req, *args, **kwargs):
        # GRADE AVERAGE WILL BE ADDED
        sql = '''SELECT C.id, C.title, U.name, La.lang_name, Le.level_title, C.start_date, C.end_date FROM levelup_api_class C, levelup_api_takes T, levelup_api_level Le, levelup_api_user U, 
        levelup_api_language La
        WHERE U.id = C.teacher_id AND T.student_id = %s AND C.id = T.class_id AND Le.id = C.level_id AND La.id = C.language_id'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        classes = dictfetchall(cursor)
        rs = json.dumps(classes, default=str)
        return Response(rs, status=status.HTTP_200_OK)


# Find Classes according to language and level
class FindClassesListAPIView(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT C.id, C.title, U.name, C.duration, Le.level_title FROM levelup_api_class C, levelup_api_level Le, levelup_api_user U
        WHERE C.language_id = %s AND C.level_id = %s AND Le.id = C.level_id AND C.teacher_id = U.id'''
        cursor = connection.cursor()
        # query parameters .../?lang="english"..
        cursor.execute(sql, [self.request.GET.get(
            'lang'), self.request.GET.get('level')])
        classes = dictfetchall(cursor)
        rs = json.dumps(classes, default=str)
        return Response(rs, status=status.HTTP_200_OK)


class ClassListAPIView(APIView):
    def get(self, req):
        #classes = Class.objects.all()
        classes = Class.objects.raw('SELECT * FROM levelup_api_class')
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = ClassSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Returns a class with classId


class ClassAPIView(APIView):
    def getClassObject(self, classId):
        try:
            # return Class.objects.get(id=classId)
            return Class.objects.raw('SELECT * FROM levelup_api_class WHERE id = %s', [classId])[0]
        except:
            return None

    def get(self, req, classId):
        classObject = self.getClassObject(classId)
        if not classObject:
            return Response(
                {"res": f"Class with id {classId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ClassSerializer(classObject)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, classId):
        classObject = self.getClassObject(classId)
        if not classObject:
            return Response(
                {"res": f"Class with id {classId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ClassSerializer(
            instance=classObject, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, classId):
        classObject = self.getClassObject(classId)
        if not classObject:
            return Response(
                {"res": f"Class with id {classId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # classObject.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_class WHERE id= %s", [classId])
        return Response(
            {"res": f"Class with id {classId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ClassBookListAPIView(APIView):
    def get(self, req):
        #classBooks = Class_Book.objects.all()
        classBooks = Class_Book.objects.raw(
            'SELECT * FROM levelup_api_class_book')
        serializer = ClassBookSerializer(classBooks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = ClassBookSerializer(data=req.data)
        if serializer.is_valid():
            # serializer.save()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO levelup_api_class_book(book_name) VALUES (%s)", [
                           serializer.validated_data['book_name']])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassBookAPIView(APIView):
    def getClassBookObject(self, classBookId):
        try:
            # return Class_Book.objects.get(id=classBookId)
            return Class_Book.objects.raw('SELECT * FROM levelup_api_class_book WHERE id = %s', [classBookId])[0]
        except:
            return None

    def get(self, req, classBookId):
        classBook = self.getClassBookObject(classBookId)
        if not classBook:
            return Response(
                {"res": f"Class Book with id {classBookId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ClassBookSerializer(classBook)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, classBookId):
        classBook = self.getClassBookObject(classBookId)
        if not classBook:
            return Response(
                {"res": f"Class Book with id {classBookId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ClassBookSerializer(
            instance=classBook, data=req.data, partial=True)
        if serializer.is_valid():
            # serializer.save()
            cursor = connection.cursor()
            cursor.execute("UPDATE levelup_api_class_book SET book_name = %s WHERE id= %s", [
                           serializer.validated_data['book_name'], classBookId])
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, classBookId):
        classBook = self.getClassBookObject(classBookId)
        if not classBook:
            return Response(
                {"res": f"Class Book with id {classBookId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # classBook.delete()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM levelup_api_class_book WHERE id= %s", [classBookId])
        return Response(
            {"res": f"Class Book with id {classBookId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class LanguageListAPIView(APIView):
    def get(self, req):
        #languages = Language.objects.all()
        languages = Language.objects.raw("SELECT * FROM levelup_api_language")
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = LanguageSerializer(data=req.data)
        if serializer.is_valid():
            cursor = connection.cursor()
            cursor.execute("INSERT INTO levelup_api_language(lang_name) VALUES (%s)", [
                           serializer.validated_data['lang_name']])
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageAPIView(APIView):
    def getLanguageObject(self, languageId):
        try:
            return Language.objects.raw('SELECT * FROM levelup_api_language WHERE id = %s', [languageId])[0]
        except:
            return None

    def get(self, req, languageId):
        language = self.getLanguageObject(languageId)
        if not language:
            return Response(
                {"res": f"Language with id {languageId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = LanguageSerializer(language)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, languageId):
        language = self.getLanguageObject(languageId)
        if not language:
            return Response(
                {"res": f"Language with id {languageId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = LanguageSerializer(
            instance=language, data=req.data, partial=True)
        if serializer.is_valid():
            cursor = connection.cursor()
            cursor.execute("UPDATE levelup_api_language SET lang_name = %s WHERE id= %s", [
                           serializer.validated_data['lang_name'], languageId])
            # serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, languageId):
        language = self.getLanguageObject(languageId)
        if not language:
            return Response(
                {"res": f"Language with id {languageId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM levelup_api_language WHERE id= %s", [languageId])
        # language.delete()
        return Response(
            {"res": f"Language with id {languageId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ForumReplyCommentListAPIView(APIView):
    def get(self, req):
        #forumReplyComments = Forum_Reply_Comment.objects.all()
        forumReplyComments = Forum_Reply_Comment.objects.raw(
            'SELECT * FROM levelup_api_forum_reply_comment')
        serializer = ForumReplyCommentSerializer(forumReplyComments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = ForumReplyCommentSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForumReplyCommentAPIView(APIView):
    def getForumReplyCommentObject(self, forumReplyCommentId):
        try:
            # return Forum_Reply_Comment.objects.get(id=forumReplyCommentId)
            return Forum_Reply_Comment.objects.raw('SELECT * FROM levelup_api_forum_reply_comment WHERE id = %s', [forumReplyCommentId])[0]
        except:
            return None

    def get(self, req, forumReplyCommentId):
        forumReplyComment = self.getForumReplyCommentObject(
            forumReplyCommentId)
        if not forumReplyComment:
            return Response(
                {"res": f"Forum Reply Comment with id {forumReplyCommentId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ForumReplyCommentSerializer(forumReplyComment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, forumReplyCommentId):
        forumReplyComment = self.getForumReplyCommentObject(
            forumReplyCommentId)
        if not forumReplyComment:
            return Response(
                {"res": f"Forum Reply Comment with id {forumReplyCommentId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ForumReplyCommentSerializer(
            instance=forumReplyComment, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, forumReplyCommentId):
        forumReplyComment = self.getForumReplyCommentObject(
            forumReplyCommentId)
        if not forumReplyComment:
            return Response(
                {"res": f"Forum Reply Comment with id {forumReplyCommentId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # forumReplyComment.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_forum_reply_comment WHERE id= %s", [
                       forumReplyCommentId])
        return Response(
            {"res": f"Forum Reply Comment with id {forumReplyCommentId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class UploadedHomeworkListAPIView(APIView):
    def get(self, req):
        #uploadedHomework = Homework_Upload.objects.all()
        uploadedHomework = Homework_Upload.objects.raw(
            'SELECT * FROM levelup_api_homework_upload')
        serializer = HomeworkUploadSerializer(
            uploadedHomework, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = HomeworkUploadSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadedHomeworkAPIView(APIView):
    def getUploadedHomeworkObject(self, uploadedHomeworkId):
        try:
            # return Homework_Upload.objects.get(id=uploadedHomeworkId)
            return Homework_Upload.objects.raw('SELECT * FROM levelup_api_homework_upload WHERE id = %s', [uploadedHomeworkId])[0]
        except:
            return None

    def get(self, req, uploadedHomeworkId):
        uploadedHomework = self.getUploadedHomeworkObject(
            uploadedHomeworkId)
        if not uploadedHomework:
            return Response(
                {"res": f"HW Upload with id {uploadedHomeworkId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = HomeworkUploadSerializer(uploadedHomework)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, uploadedHomeworkId):
        uploadedHomework = self.getUploadedHomeworkObject(
            uploadedHomeworkId)
        if not uploadedHomework:
            return Response(
                {"res": f"HW Upload with id {uploadedHomeworkId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = HomeworkUploadSerializer(
            instance=uploadedHomework, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, uploadedHomeworkId):
        uploadedHomework = self.getForumReplyCommentObject(
            uploadedHomeworkId)
        if not uploadedHomework:
            return Response(
                {"res": f"HW Upload with id {uploadedHomeworkId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # uploadedHomework.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_homework_upload WHERE id= %s", [
                       uploadedHomeworkId])
        return Response(
            {"res": f"HW Upload with id {uploadedHomeworkId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ForumReplyListAPIView(APIView):
    def get(self, req):
        #forumReplies = Forum_Reply.objects.all()
        forumReplies = Forum_Reply.objects.raw(
            'SELECT * FROM levelup_api_forum_reply')
        serializer = ForumReplySerializer(
            forumReplies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = ForumReplySerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForumReplyAPIView(APIView):
    def getForumReplyObject(self, forumReplyId):
        try:
            # return Forum_Reply.objects.get(id=forumReplyId)
            return Forum_Reply.objects.raw('SELECT * FROM levelup_api_forum_reply WHERE id = %s', [forumReplyId])[0]

        except:
            return None

    def get(self, req, forumReplyId):
        forumReply = self.getForumReplyObject(
            forumReplyId)
        if not forumReply:
            return Response(
                {"res": f"Forum Reply with id {forumReplyId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ForumReplySerializer(forumReply)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, forumReplyId):
        forumReply = self.getForumReplyObject(
            forumReplyId)
        if not forumReply:
            return Response(
                {"res": f"Forum Reply with id {forumReplyId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ForumReplySerializer(
            instance=forumReply, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, forumReplyId):
        forumReply = self.getForumReplyObject(
            forumReplyId)
        if not forumReply:
            return Response(
                {"res": f"Forum Reply with id {forumReplyId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # forumReply.delete()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM levelup_api_forum_reply WHERE id= %s", [forumReplyId])
        return Response(
            {"res": f"Forum Reply with id {forumReplyId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ClassRatingListAPIView(APIView):
    def get(self, req):
        #classRatings = Rate_Class_Details.objects.all()
        classRatings = Rate_Class_Details.objects.raw(
            'SELECT * FROM levelup_api_rate_class_details')
        serializer = RateClassDetailsSerializer(
            classRatings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = RateClassDetailsSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassRatingAPIView(APIView):
    def getClassRatingObject(self, classRatingId):
        try:
            # return Rate_Class_Details.objects.get(id=forumReplyId)
            Rate_Class_Details.objects.raw(
                'SELECT * FROM levelup_api_rate_class_details WHERE id = %s', [classRatingId])[0]
        except:
            return None

    def get(self, req, classRatingId):
        classRating = self.getClassRatingObject(
            classRatingId)
        if not classRating:
            return Response(
                {"res": f"Class Rating with id {classRatingId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RateClassDetailsSerializer(classRating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, classRatingId):
        classRating = self.getClassRatingObject(
            classRatingId)
        if not classRating:
            return Response(
                {"res": f"Class Rating with id {classRatingId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RateClassDetailsSerializer(
            instance=classRating, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, classRatingId):
        classRating = self.getClassRatingObject(
            classRatingId)
        if not classRating:
            return Response(
                {"res": f"Class Rating with id {classRatingId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # classRating.delete()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM levelup_api_rate_class_details WHERE id= %s", [classRatingId])
        return Response(
            {"res": f"Class Rating with id {classRatingId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )
