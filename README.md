# 📹youtube-summarizer

YouTube Summarizer is an automated tool that fetches transcripts from YouTube videos and generates concise summaries using AI language models. Additionally, it enables users to ask follow-up questions about the video content, providing contextualized answers based on the transcript. This tool is perfect for quickly extracting key information from lengthy videos and diving into specific topics without having to watch the entire video. 🎥

🌟 Features
📝 Summary Generation: Retrieves the transcript from YouTube videos and produces a clear, concise summary of the content.
💬 Real-Time Interaction: Allows you to ask additional questions about the video, receiving detailed answers in real-time.
🎩 Typing Animation: Displays responses with a typewriter effect in the terminal for a visually engaging experience.
🤖 Generative AI: Integrates advanced language models to accurately summarize and answer questions naturally.
🛠️ Technologies
Python
YouTube Data API for transcript retrieval
Google Generative Language API for summarization and question-answering
🚀 Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your_username/youtube-summarizer.git
cd youtube-summarizer
Install requirements:

bash
Copy code
pip install -r requirements.txt
Set up the API Key as an environment variable:

bash
Copy code
export YOUR_API_KEY_ENV_VAR="your_api_key"
Run the script:

bash
Copy code
python youtube_summarizer.py
📖 Usage
Enter the YouTube video link or ID when prompted. This specifies the video you want to summarize.

Summary Generation: The tool will automatically generate a summary based on the video’s transcript.

Ask Questions: You can ask questions about the video content in the terminal, and the tool will respond with context-based answers.

To exit, simply type quit, exit, or bye.
