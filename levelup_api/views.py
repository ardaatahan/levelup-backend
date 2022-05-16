from distutils.command.upload import upload
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
import json

from .models import *
from .serializers import *


class SystemUserListView(APIView):
    def get(self, req, *args, **kwargs):
        system_users = System_User.objects.all()
        serializer = SystemUserSerializer(system_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, *args, **kwargs):
        data = {}


class SystemUserAPIView(APIView):
    def get(self, req, systemUserId, *args, **kwargs):
        try:
            system_user = System_User.objects.get(id=systemUserId)
        except:
            system_user = None
        if not system_user:
            return Response(
                {"res": f"System User with id {systemUserId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SystemUserSerializer(system_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, systemUserId, *args, **kwargs):
        pass

    def delete(self, req, systemUserId, *args, **kwargs):
        pass


class SpeakingExerciseListView(APIView):
    def get(self, req, *args, **kwargs):
        #speaking_exercises = Speaking_Exercise.objects.all()
        speaking_exercises = Speaking_Exercise.objects.raw('SELECT * FROM levelup_api_speaking_exercise')
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


class SpeakingExerciseAPIView(APIView):
    def getExerciseObject(self, exercise_id):
        try:
            #return Speaking_Exercise.objects.get(id=exercise_id)      
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
        #exerciseObject.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_speaking_exercise WHERE id= %s", [exercise_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

# Returns all speaking exercises info for a language native
class SpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.name, Sp.exercise_datetime, Sp.exercise_link FROM levelup_api_language_native as L, levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U WHERE L.user_id = %s AND L.user_id = Sp.language_native_id AND Sp.student_id = U.id'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = cursor.fetchall()
        rs = json.dumps(dict(speaking_exercises)) # rs is a list of tuples, json.dumps converts it to json object
        return Response(rs, status=status.HTTP_200_OK)
    
# Returns only ungraded speaking exercises info for a language native
class UngradedSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.name, Sp.exercise_datetime, Sp.exercise_link FROM levelup_api_language_native as L, levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U WHERE L.user_id = %s AND L.user_id = Sp.language_native_id AND Sp.student_id = U.id Sp.grade IS NULL'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = cursor.fetchall()
        rs = json.dumps(dict(speaking_exercises))
        return Response(rs, status=status.HTTP_200_OK)
    
# Returns only graded speaking exercises info for a language native
class GradedSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.name, Sp.exercise_datetime, Sp.exercise_link FROM levelup_api_language_native as L, levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U WHERE L.user_id = %s AND L.user_id = Sp.language_native_id AND Sp.student_id = U.id Sp.grade IS NOT NULL'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = cursor.fetchall()
        rs = json.dumps(dict(speaking_exercises))
        return Response(rs, status=status.HTTP_200_OK)
    
# Returns only upcoming speaking exercises info for a language native
class UpcomingSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.name, Sp.exercise_datetime, Sp.exercise_link FROM levelup_api_language_native as L, levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U WHERE L.user_id = %s AND L.user_id = Sp.language_native_id AND Sp.student_id = U.id AND Sp.exercise_datetime > NOW()'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = cursor.fetchall()
        rs = json.dumps(dict(speaking_exercises))
        return Response(rs, status=status.HTTP_200_OK)
    
# Returns only past speaking exercises info for a language native
class PastSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.name, Sp.exercise_datetime, Sp.exercise_link FROM levelup_api_language_native as L, levelup_api_speaking_exercise as Sp, 
        levelup_api_user as U WHERE L.user_id = %s AND L.user_id = Sp.language_native_id AND Sp.student_id = U.id AND Sp.exercise_datetime < NOW()'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        speaking_exercises = cursor.fetchall()
        rs = json.dumps(dict(speaking_exercises))
        return Response(rs, status=status.HTTP_200_OK)
    
# Returns only pending speaking exercise requests info for a language native
class RequestedSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.name, R.requested_datetime, R.additional_notes FROM levelup_api_language_native L, levelup_api_request_exercise R,
        levelup_api_user U WHERE L.user_id = %s AND L.user_id = R.language_native_id AND R.student_id = U.id AND R.status IS NULL'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id])
        requests = cursor.fetchall()
        rs = json.dumps(dict(requests))
        return Response(rs, status=status.HTTP_200_OK)
    
# Returns only declined speaking exercise requests info for a language native
class DeclinedRequestedSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.name, R.requested_datetime, R.additional_notes FROM levelup_api_language_native L, levelup_api_request_exercise R,
        levelup_api_user U WHERE L.user_id = %s AND L.user_id = R.language_native_id AND R.student_id = U.id AND R.status=%s'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id, 'DECLINED'])
        requests = cursor.fetchall()
        rs = json.dumps(dict(requests))
        return Response(rs, status=status.HTTP_200_OK)
    
# Returns only accepted speaking exercise requests info for a language native
class AcceptedRequestedSpeakingExercisesListViewForLanguageNative(APIView):
    def get(self, req, *args, **kwargs):
        sql = '''SELECT U.name, R.requested_datetime, R.additional_notes FROM levelup_api_language_native L, levelup_api_request_exercise R,
        levelup_api_user U WHERE L.user_id = %s AND L.user_id = R.language_native_id AND R.student_id = U.id AND R.status=%s'''
        cursor = connection.cursor()
        cursor.execute(sql, [req.user.id, 'ACCEPTED'])
        requests = cursor.fetchall()
        rs = json.dumps(dict(requests))
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
        #homeworkObject.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_homework WHERE id= %s", [homework_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class ForumTopicListView(APIView):
    def get(self, req, *args, **kwargs):
        #topics = Forum_Topic.objects.all()
        topics = Forum_Topic.objects.raw('SELECT * FROM levelup_api_forum_topic')
        serializer = ForumTopicSerializer(topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, *args, **kwargs):
        serializer = ForumTopicSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForumSearchByTopicListView(APIView):
    pass
class ForumTopicAPIView(APIView):
    def getForumTopicObject(self, topic_id):
        try:
           # return Forum_Topic.objects.get(id=topic_id)
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
        #forumTopicObject.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_forum_topic WHERE id= %s", [topic_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class RequestExerciseListView(APIView):
    def get(self, req, *args, **kwargs):
        #requests = Request_Exercise.objects.all()
        requests = Request_Exercise.objects.raw('SELECT * FROM levelup_api_request_exercise')
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
            #return Request_Exercise.objects.get(id=request_id)
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
        #requestObject.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_request_exercise WHERE id= %s", [request_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


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
            cursor.execute("INSERT INTO levelup_api_level(level_title) VALUES (%s)", [serializer.validated_data['level_title']])
            #serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LevelAPIView(APIView):
    def getLevelObject(self, level_id):
        try:
            #return Level.objects.get(id=level_id)
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
            cursor.execute("UPDATE levelup_api_level SET level_title = %s WHERE id= %s", [serializer.validated_data['level_title'], level_id])
            #serializer.save()
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
        cursor.execute("DELETE FROM levelup_api_level WHERE id= %s", [level_id])
        #print(res)
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
            cursor.execute("INSERT INTO levelup_api_tag(tag_title) VALUES (%s)", [serializer.validated_data['tag_title']])
            #serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagAPIView(APIView):
    def getTagObject(self, tag_id):
        try:
            #return Tag.objects.get(id=tag_id)
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
            cursor.execute("UPDATE levelup_api_tag SET tag_title = %s WHERE id= %s", [serializer.validated_data['tag_title'], tag_id])
            #serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, tag_id, *args, **kwargs):
        tagObject = self.getTagObject(tag_id)
        if not tagObject:
            return Response(
                {"res": f"Object with Tag id {tag_id} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        #tagObject.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_tag WHERE id= %s", [tag_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class RateExerciseDetailsListView(APIView):
    def get(self, req, *args, **kwargs):
        #rateExerciseDetails = Rate_Exercise_Details.objects.all()
        rateExerciseDetails = Rate_Exercise_Details.objects.raw('SELECT * FROM levelup_api_rate_exercise_details')
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
            #return Rate_Exercise_Details.objects.get(id=detail_id)
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
        #exerciseDetailObject.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_rate_exercise_details WHERE id= %s", [detail_id])
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


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


class ClassAPIView(APIView):
    def getClassObject(self, classId):
        try:
            #return Class.objects.get(id=classId)
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
        serializer = UserSerializer(classObject)
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
        #classObject.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_class WHERE id= %s", [classId])
        return Response(
            {"res": f"Class with id {classId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ClassBookListAPIView(APIView):
    def get(self, req):
        #classBooks = Class_Book.objects.all()
        classBooks = Class_Book.objects.raw('SELECT * FROM levelup_api_class_book')
        serializer = ClassBookSerializer(classBooks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = ClassBookSerializer(data=req.data)
        if serializer.is_valid():
            #serializer.save()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO levelup_api_class_book(book_name) VALUES (%s)", [serializer.validated_data['book_name']])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassBookAPIView(APIView):
    def getClassBookObject(self, classBookId):
        try:
            #return Class_Book.objects.get(id=classBookId)
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
            #serializer.save()
            cursor = connection.cursor()
            cursor.execute("UPDATE levelup_api_class_book SET book_name = %s WHERE id= %s", [serializer.validated_data['book_name'], classBookId])
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, classBookId):
        classBook = self.getClassBookObject(classBookId)
        if not classBook:
            return Response(
                {"res": f"Class Book with id {classBookId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        #classBook.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_class_book WHERE id= %s", [classBookId])
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
            cursor.execute("INSERT INTO levelup_api_language(lang_name) VALUES (%s)", [serializer.validated_data['lang_name']])
            #serializer.save()
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
            cursor.execute("UPDATE levelup_api_language SET lang_name = %s WHERE id= %s", [serializer.validated_data['lang_name'], languageId])
            #serializer.save()
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
        cursor.execute("DELETE FROM levelup_api_language WHERE id= %s", [languageId])
        #language.delete()
        return Response(
            {"res": f"Language with id {languageId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ForumReplyCommentListAPIView(APIView):
    def get(self, req):
        #forumReplyComments = Forum_Reply_Comment.objects.all()
        forumReplyComments = Forum_Reply_Comment.objects.raw('SELECT * FROM levelup_api_forum_reply_comment')
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
            #return Forum_Reply_Comment.objects.get(id=forumReplyCommentId)
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
        #forumReplyComment.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_forum_reply_comment WHERE id= %s", [forumReplyCommentId])
        return Response(
            {"res": f"Forum Reply Comment with id {forumReplyCommentId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class UploadedHomeworkListAPIView(APIView):
    def get(self, req):
        #uploadedHomework = Homework_Upload.objects.all()
        uploadedHomework = Homework_Upload.objects.raw('SELECT * FROM levelup_api_homework_upload')
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
            #return Homework_Upload.objects.get(id=uploadedHomeworkId)
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
        #uploadedHomework.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_homework_upload WHERE id= %s", [uploadedHomeworkId])
        return Response(
            {"res": f"HW Upload with id {uploadedHomeworkId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ForumReplyListAPIView(APIView):
    def get(self, req):
        #forumReplies = Forum_Reply.objects.all()
        forumReplies = Forum_Reply.objects.raw('SELECT * FROM levelup_api_forum_reply')
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
            #return Forum_Reply.objects.get(id=forumReplyId)
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
        #forumReply.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_forum_reply WHERE id= %s", [forumReplyId])
        return Response(
            {"res": f"Forum Reply with id {forumReplyId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ClassRatingListAPIView(APIView):
    def get(self, req):
        #classRatings = Rate_Class_Details.objects.all()
        classRatings = Rate_Class_Details.objects.raw('SELECT * FROM levelup_api_rate_class_details')
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
            #return Rate_Class_Details.objects.get(id=forumReplyId)
            Rate_Class_Details.objects.raw('SELECT * FROM levelup_api_rate_class_details WHERE id = %s', [classRatingId])[0]
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
        #classRating.delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelup_api_rate_class_details WHERE id= %s", [classRatingId])
        return Response(
            {"res": f"Class Rating with id {classRatingId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )
