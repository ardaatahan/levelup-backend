from django.urls import path
from .views import *

urlpatterns = [
    path("classes", ClassListAPIView.as_view()),
    path("classes/<int:classId>", ClassAPIView.as_view()),
    path("class_books", ClassBookListAPIView.as_view()),
    path("class_books/<int:classBookId>", ClassBookAPIView.as_view()),
    path("languages", LanguageListAPIView.as_view()),
    path("languages/<int:languageId>", LanguageAPIView.as_view()),
    path("forum_reply_comments", ForumReplyCommentListAPIView.as_view()),
    path("forum_reply_comments/<int:forumReplyCommentId>",
         ForumReplyCommentAPIView.as_view()),
    path("uploaded_homework", UploadedHomeworkListAPIView.as_view()),
    path("uploaded_homework/<int:uploadedHomeworkId>",
         UploadedHomeworkAPIView.as_view()),
    path("forum_replies", ForumReplyListAPIView.as_view()),
    path("forum_replies/<int:forumReplyId>", ForumReplyAPIView.as_view()),
    path("class_ratings", ClassRatingListAPIView.as_view()),
    path("class_ratings/<int:classRatingId>", ClassRatingAPIView.as_view()),
]
