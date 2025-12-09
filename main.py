from youtube_transcript_api import YouTubeTranscriptApi
import json
from google import genai
from pydantic import BaseModel
from youtube_transcript_api.formatters import SRTFormatter
import os
import srt
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

def get_transcript(video_ID, start_time=0, end_time=120, ): #start_time and end_time don't work yet

    #video_url = 'https://youtu.be/Oo9EbArcQ1c'

    #video_ID = 'Oo9EbArcQ1c' #get this automatically later

    ytt_api = YouTubeTranscriptApi()
    snippets = ytt_api.fetch(video_ID).snippets

    formatter = SRTFormatter()
    srt_formatted = formatter.format_transcript(snippets)

    dir_create = Path(f"data/raw/{video_ID}.srt")
    dir_create.parent.mkdir(exist_ok=True, parents=True)

    with open(f'data/raw/{video_ID}.srt', 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_formatted)

    final_transcript = ''
    for transcript in snippets:
        if transcript.start == 0:
            if transcript.start >= 0 and (transcript.start + transcript.duration)<=end_time:
                final_transcript += (str(transcript).replace('FetchedTranscriptSnippet', ''))
        else:
            if transcript.start >= 0 and transcript.start>=start_time and (transcript.start + transcript.duration)<=end_time:
                final_transcript += (str(transcript).replace('FetchedTranscriptSnippet', ''))
    

def generate_video_ideas(video_ID, output_file, number=10, special_prompt = ""): 
    ytt_api = YouTubeTranscriptApi()
    snippets = ytt_api.fetch(video_ID).snippets
    client = genai.Client(api_key=GEMINI_API_KEY)


    class Template(BaseModel):
        title: str
        start_time: float
        duration: float
        video_generated: bool
        video_published: bool

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents=f"""
        Act as a professional video editor specializing in high-retention YouTube Shorts and TikToks. 
        Analyze the provided transcript and extract {number} candidates for viral shorts.
        
        For each candidate, you must meet these criteria:

        1. DURATION: Between 15 and 60 seconds (optimized for ~30 seconds preferred).
        2. HOOK: The title (With emojis if appropriate) and the first 3 seconds must contain a strong hook (a startling statement, high stakes, or intense curiosity gap).
        3. NARRATIVE: The clip must stand alone with a clear beginning, middle, and end (or loop seamlessly).

        start time and total duration to be cut from the start time, make sure the video is between 15-60 seconds, keep video_generated and video_published as false. {special_prompt} {snippets}
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Template],
        })

    print(response.text)

    try:
        with open(output_file, 'w') as file:
            data = json.load(file)
            print(f'Loaded data: {data}')
    except:
        #print(e.message)
        data = []

    #gen_vid = json.loads(response.text)
    data.append(json.loads(response.text))

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)


    #print(response)

#video_ID = 'EIhIIsPMehg'
video_ID = input("Enter video ID: ")
get_transcript(video_ID)
print("Generated transcripts!")
generate_video_ideas(video_ID, f'data/raw/{video_ID}_ideas.json', 15, "Leave the first 5 minutes")
print("Generated video ideas!")
