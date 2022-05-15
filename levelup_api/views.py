from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


# class UserListView(APIView):
#     def get(self, req, *args, **kwargs):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, req, *args, **kwargs):
#         data = {

#         }


# class UserAPIView(APIView):
#     def get(self, req, userId, *args, **kwargs):
#         try:
#             user = User.objects.get(id=userId)
#         except:
#             user = None
#         if not user:
#             return Response(
#                 {"res": f"User with id {userId} does not exists"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, req, userId, *args, **kwargs):
#         pass

#     def delete(self, req, userId, *args, **kwargs):
#         pass

class ClassListAPIView(APIView):
    def get(self, req):
        classes = Class.objects.all()
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
            return Class.objects.get(id=classId)
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
        classObject.delete()
        return Response(
            {"res": f"Class with id {classId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ClassBookListAPIView(APIView):
    def get(self, req):
        classBooks = Class_Book.objects.all()
        serializer = ClassBookSerializer(classBooks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = ClassBookSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassBookAPIView(APIView):
    def getClassBookObject(self, classBookId):
        try:
            return Class_Book.objects.get(id=classBookId)
        except:
            return None

    def get(self, req, classBookId):
        classBook = self.getClassBookObject(classBookId)
        if not classBook:
            return Response(
                {"res": f"Class with id {classBookId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ClassBookSerializer(classBook)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, classBookId):
        classBook = self.getClassBookObject(classBookId)
        if not classBook:
            return Response(
                {"res": f"Class with id {classBookId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ClassBookSerializer(
            instance=classBook, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, classBookId):
        classBook = self.getClassBookObject(classBookId)
        if not classBook:
            return Response(
                {"res": f"Class with id {classBookId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        classBook.delete()
        return Response(
            {"res": f"Class with id {classBookId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class LanguageListAPIView(APIView):
    def get(self, req):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = LanguageSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageAPIView(APIView):
    def getLanguageObject(self, languageId):
        try:
            return Language.objects.get(id=languageId)
        except:
            return None

    def get(self, req, languageId):
        language = self.getLanguageObject(languageId)
        if not language:
            return Response(
                {"res": f"Class with id {languageId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = LanguageSerializer(language)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, languageId):
        language = self.getLanguageObject(languageId)
        if not language:
            return Response(
                {"res": f"Class with id {languageId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = LanguageSerializer(
            instance=language, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, languageId):
        language = self.getLanguageObject(languageId)
        if not language:
            return Response(
                {"res": f"Class with id {languageId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        language.delete()
        return Response(
            {"res": f"Class with id {languageId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ForumReplyCommentListAPIView(APIView):
    def get(self, req):
        forumReplyComments = Forum_Reply_Comment.objects.all()
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
            return Forum_Reply_Comment.objects.get(id=forumReplyCommentId)
        except:
            return None

    def get(self, req, forumReplyCommentId):
        forumReplyComment = self.getForumReplyCommentObject(
            forumReplyCommentId)
        if not forumReplyComment:
            return Response(
                {"res": f"Class with id {forumReplyCommentId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ForumReplyCommentSerializer(forumReplyComment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, forumReplyCommentId):
        forumReplyComment = self.getForumReplyCommentObject(
            forumReplyCommentId)
        if not forumReplyComment:
            return Response(
                {"res": f"Class with id {forumReplyCommentId} does not exists"},
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
                {"res": f"Class with id {forumReplyCommentId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        forumReplyComment.delete()
        return Response(
            {"res": f"Class with id {forumReplyCommentId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class UploadedHomeworkListAPIView(APIView):
    def get(self, req):
        uploadedHomework = Homework_Upload.objects.all()
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
            return Homework_Upload.objects.get(id=uploadedHomeworkId)
        except:
            return None

    def get(self, req, uploadedHomeworkId):
        uploadedHomework = self.getUploadedHomeworkObject(
            uploadedHomeworkId)
        if not uploadedHomework:
            return Response(
                {"res": f"Class with id {uploadedHomeworkId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = HomeworkUploadSerializer(uploadedHomework)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, uploadedHomeworkId):
        uploadedHomework = self.getUploadedHomeworkObject(
            uploadedHomeworkId)
        if not uploadedHomework:
            return Response(
                {"res": f"Class with id {uploadedHomeworkId} does not exists"},
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
                {"res": f"Class with id {uploadedHomeworkId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        uploadedHomework.delete()
        return Response(
            {"res": f"Class with id {uploadedHomeworkId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ForumReplyListAPIView(APIView):
    def get(self, req):
        forumReplies = Forum_Reply.objects.all()
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
            return Forum_Reply.objects.get(id=forumReplyId)
        except:
            return None

    def get(self, req, forumReplyId):
        forumReply = self.getForumReplyObject(
            forumReplyId)
        if not forumReply:
            return Response(
                {"res": f"Class with id {forumReplyId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ForumReplySerializer(forumReply)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, forumReplyId):
        forumReply = self.getForumReplyObject(
            forumReplyId)
        if not forumReply:
            return Response(
                {"res": f"Class with id {forumReplyId} does not exists"},
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
                {"res": f"Class with id {forumReplyId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        forumReply.delete()
        return Response(
            {"res": f"Class with id {forumReplyId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )


class ClassRatingListAPIView(APIView):
    def get(self, req):
        classRatings = Rate_Class_Details.objects.all()
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
    def getClassRatingObject(self, forumReplyId):
        try:
            return Rate_Class_Details.objects.get(id=forumReplyId)
        except:
            return None

    def get(self, req, classRatingId):
        classRating = self.getClassRatingObject(
            classRatingId)
        if not classRating:
            return Response(
                {"res": f"Class with id {classRatingId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RateClassDetailsSerializer(classRating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, classRatingId):
        classRating = self.getClassRatingObject(
            classRatingId)
        if not classRating:
            return Response(
                {"res": f"Class with id {classRatingId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RateClassDetailsSerializer(
            instance=classRating, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, classRatingId):
        classRating = self.getForumReplyObject(
            classRatingId)
        if not classRating:
            return Response(
                {"res": f"Class with id {classRatingId} does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        classRating.delete()
        return Response(
            {"res": f"Class with id {classRatingId} has been deleted successfully"},
            status=status.HTTP_200_OK
        )
