from django.db import models
from django.utils import timezone

class Task(models.Model):
    video_input = models.CharField(max_length=255)
    lang = models.CharField(max_length=2, default='en')
    created_at = models.DateTimeField(auto_now_add=True)  # Only use auto_now_add here
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task for video: {self.video_input[:30]}..."
