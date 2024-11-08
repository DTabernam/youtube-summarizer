from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import TaskSerializer
from youtube_transcript_api import YouTubeTranscriptApi
import re
import json
import os
import requests
from django.conf import settings
from django.conf import settings

class VideoSummaryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        video_input = request.query_params.get('name')
        lang= request.query_params.get('lang')
        if video_input:
            request.data['video_input'] = video_input

        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        video_input = serializer.validated_data['video_input']

        video_id = self.extract_video_id(video_input)
        if not video_id:
            return Response({"error": "Invalid YouTube URL or video ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transcript = self.get_transcript(video_id, lang)
            summary = self.generate_summary(transcript)
            return Response({"summary": summary, "transcript": transcript}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def extract_video_id(self, video_input):
        youtube_regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?:live\/)?(?:(?!videos)(?!channel)(?!user)(?!playlist)(?!embed)(?!v)(?!live)(?!shorts)(?!watch)(?:\S+))?"
        match = re.search(youtube_regex, video_input)
        return match.group(1) if match else video_input

    def get_transcript(self, video_id, lang):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
            return json.dumps(transcript, ensure_ascii=False, indent=4)
        except Exception as e:
            raise Exception(f"Error fetching transcript: {str(e)}")

    def generate_summary(self, transcript):
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise Exception("Gemixni API key not configured")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": f"Summarize this transcript: {transcript}"}]}]
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code}")

        try:
           return response.json()['candidates'][0]['content']['parts'][0]['text']
        except (IndexError, KeyError):
            raise Exception("Error extracting summary from Gemini response")
        
        
class AskQuestionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        question = request.data.get('question')
        transcript = request.data.get('transcript')

        if not question or not transcript:
            return Response({"error": "Question and transcript are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            answer = self.generate_answer(question, transcript)
            return Response({"answer": answer}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generate_answer(self, question, transcript):
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise Exception("Gemini API key not configured")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": f"You are a summarization ia , you will get transcripts from a video you dont need to summarize it because you have already did : {transcript} now you can answer this question or opinion about the video or a related subject : {question}"}]}]
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code}")

        try:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except (IndexError, KeyError):
            raise Exception("Error extracting answer from Gemini response")
