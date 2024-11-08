"""from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from .models import Task

class VideoSummaryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('your_app.views.VideoSummaryAPIView.get_transcript')
    @patch('your_app.views.VideoSummaryAPIView.generate_summary')
    def test_video_summary_api(self, mock_generate_summary, mock_get_transcript):
        mock_get_transcript.return_value = "Mocked transcript"
        mock_generate_summary.return_value = "Mocked summary"

        data = {
            "video_input": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "lang": "en"
        }
        response = self.client.post('/api/video-summary/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('summary', response.data)
        self.assertIn('transcript', response.data)

    def test_invalid_video_input(self):
        data = {"video_input": ""}
        response = self.client.post('/api/video-summary/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)"""