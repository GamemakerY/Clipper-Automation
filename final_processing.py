import ffmpeg
import json
from pycaps import TemplateLoader
import os
from pathlib import Path

def create_clips(video_ID, Num=0):
    video_path = f'data/raw/{video_ID}_cropped.mp4'

    probe = ffmpeg.probe(video_path)
    video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)

    r_frame_rate_str = video_stream.get('r_frame_rate')
    if r_frame_rate_str:
        num, den = map(int, r_frame_rate_str.split('/'))
        fps = num / den
    

    with open(f'data/raw/{video_ID}_ideas.json', 'r') as file:
        data = json.load(file)
    
    i=0
    for item in data[0]:
        if data[0][i]['video_generated'] == False:
            start_time = data[0][i]['start_time']
            end_time= (data[0][i]['start_time'] + data[0][i]['duration'])
            input_file = ffmpeg.input(f'data/raw/{video_ID}_cropped.mp4')
            pts = "PTS-STARTPTS"
            video = input_file.trim(start = start_time, end = end_time).setpts(pts)
            audio = (input_file
            .filter_("atrim", start = start_time, end = end_time)
            .filter_("asetpts", pts))
            
            video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
            
            output_file = ffmpeg.output(video_and_audio,f'data/raw/output_{video_ID}_{i}.mp4',  vcodec='h264_qsv', preset='veryfast') #Find a way to generalise hardware acceleration later for anyone to use
            ffmpeg.run(output_file)

            add_captions(f'data/raw/output_{video_ID}_{i}.mp4', f'data/processed/final_{video_ID}_{i}.mp4')
            data[0][i]["video_generated"] = True
            print(f"Successfully generated video- {i}")

        i+=1

    with open(f'data/raw/{video_ID}_ideas.json', 'w') as file:
        json.dump(data, file, indent=4)

    
    #data.append(json.loads(data))

    try:
        with open(f'data/raw/{video_ID}_ideas.json', 'w') as file:
            json.dump(data, file, indent=4)
            print(f"File 'data/raw/{video_ID}_ideas.json' updated.")
    
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")




def add_captions(input_path, output_path):
    builder = TemplateLoader("hype").with_input_video(input_path).load(False)
    builder.with_output_video(output_path)
    pipeline = builder.build()
    pipeline.run()


video_ID = input("Enter video ID: ")

create_clips(video_ID)

#add_captions(f"data/raw/{video_ID}_cropped.mp4", f"data/processed/{video_ID}_final.mp4")


#For loop after importing from json file here


#output_file = (ffmpeg.output(input_file.trim(start_frame=fps*(data[0][0]['start_time']), end_frame=fps*(data[0][0]['start_time'] + data[0][0]['duration'])).setpts('PTS-STARTPTS'), 'data/processed/output_Oo9EbArcQ1c_1.mp4'))

