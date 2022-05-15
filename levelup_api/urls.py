from django.urls import path, include
from .views import *

urlpatterns = [
    #path("system_users", SystemUserListView.as_view()),
    #path("system_users/<int:systemUserId>", SystemUserAPIView.as_view()),
    path("speaking_exercises", SpeakingExerciseListView.as_view()),
    path("speaking_exercises/<int:exercise_id>", SpeakingExerciseAPIView.as_view()),
    path("homeworks", HomeworkListView.as_view()),
    path("homeworks/<int:homework_id>", HomeworkAPIView.as_view()),
    path("forum_topics", ForumTopicListView.as_view()),
    path("forum_topics/<int:topic_id>", ForumTopicAPIView.as_view()),
    path("requested_exercises", RequestExerciseListView.as_view()),
    path("requested_exercises/<int:request_id>", RequestExerciseAPIView.as_view()),
    path("levels", LevelListView.as_view()),
    path("levels/<int:level_id>", LevelAPIView.as_view()),
    path("tags", TagListView.as_view()),
    path("tags/<int:tag_id>", TagAPIView.as_view()),
    path("rated_exercise_details", RateExerciseDetailsListView.as_view()),
    path("rated_exercise_details/<int:detail_id>", RateExerciseDetailsAPIView.as_view()),
]
