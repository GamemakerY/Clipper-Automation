from moviepy import *
import os
import ffmpeg
import pycaps
from pycaps import TemplateLoader
import yt_dlp


#input = ffmpeg.input('test1.mp4')

#try:
def download_video(video_ID, output_path='data/raw/', max_resolution='720p'):
    url = f'https://youtu.be/{video_ID}'
    ydl_opts = {
        'format': 'best[ext=mp4][vcodec!=none][acodec!=none]',
        'outtmpl': f'{output_path}{video_ID}.%(ext)s',
        'noplaylist': True,
        'merge_output_format': 'mp4', 
        'postprocessors': [],         # Explicitly disable any post-processing
        'verbose': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Attempting to download best progressive MP4 stream...")
            info_dict = ydl.extract_info(url, download=True)
            print(f"\nDownload completed for: {info_dict.get('title', 'Video')}")
            print(f"File resolution: {info_dict.get('height')}p (No merging required)")
    except Exception as e:
        print(f"\nAn error occured: {e}")


def crop_video(input_path, output_path):
    probe = ffmpeg.probe(input_path)

    video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video') ###

     
    in_w = int(video_stream['width'])
    in_h = int(video_stream['height'])

    stream = ffmpeg.input(input_path)

    audio_stream = stream.audio

    #cropped_video = ffmpeg.crop(stream, (in_w-((9/16)*in_h)/2), 0, (9/16)*in_h, in_h)
    cropped_video = (ffmpeg.crop(stream, (in_w-in_h)/2, 0, in_h, in_h).
                     filter('pad', h=(16/9)*in_h, y=((16/9)*in_h/2)))

    #cropped_video = ffmpeg.filter(stream, 'pad', h=(16/9)*in_h, y=((16/9)*in_h/2))
    try:
        cropped_video = ffmpeg.output(cropped_video, audio_stream, output_path, 
                                      vcodec='h264_qsv')        # Apparently it's decent)
        ffmpeg.run(cropped_video)
    except ffmpeg.Error as e:
        print(e.stderr)


video_ID = 'EIhIIsPMehg'

download_video(video_ID)

crop_video(f"data/raw/{video_ID}.mp4", f"data/raw/{video_ID}_cropped.mp4")

#trim first --> crop --> captions

#crop_video("test1.mp4", "media/test1_realcrop.mp4")


#DON'T DO SEPARATELY LATER

