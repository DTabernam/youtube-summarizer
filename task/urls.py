from django.urls import path
from .views import VideoSummaryAPIView, AskQuestionAPIView

urlpatterns = [
    path('video-summary/', VideoSummaryAPIView.as_view(), name='video_summary'),
    path('ask-question/', AskQuestionAPIView.as_view(), name='ask_question'),
]