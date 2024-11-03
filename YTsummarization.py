import re
from youtube_transcript_api import YouTubeTranscriptApi
import os
import json
import requests
video_input = input('\033[1;33m'+"Please input the YouTube video link or ID: ")
video_id = re.sub(r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=)?", "", video_input)
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es', 'en'])
with open(f"{video_id}_transcription.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(transcript, ensure_ascii=False, indent=4))
with open(f"{video_id}_transcription.txt", "r", encoding="utf-8") as f:
    transcript_content = f.read()
print(f"Transcription saved as {video_id}_transcription.txt")

text_content = f"You are a summarization ia , you will get transcripts from a video and you will summarize it : {transcript_content}" 
data = {
    "contents": [
        {
            "parts": [
                {"text": text_content}
            ]
        }
    ]
}

api_key = os.getenv("YOUR_API_KEY_ENV_VAR")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
headers = {
    "Content-Type": "application/json"
}
response = requests.post(url, headers=headers, data=json.dumps(data))
#print("Status Code:", response.status_code)
#print("Response:", response.json())
if response.status_code == 200:
        try:
            answer = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("\033[;36m"+answer)
        except (IndexError, KeyError) as e:
            print("Error extracting text:", e)
else:
    print("Error:", response.status_code, response.text)
while True : 
    
    Entry = str (input("\033[1;33m"+"Ask me something about the video : "))
    if Entry == "Quit" or Entry == "exit" or Entry == "quit" or Entry == "bye":
        break
    else : 
        text_content = f"You are a summarization ia , you will get transcripts from a video you dont need to summarize it because you have already did : {transcript_content} in case you need it here is your summary {answer} now you can answer this question about the video : {Entry}" 
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": text_content}
                    ]
                }
            ]
        }

        api_key = os.getenv("YOUR_API_KEY_ENV_VAR")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            new_answer = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("\033[;36m"+new_answer)
        #print("Status Code:", response.status_code)
        #print("Response:", response.json())
        