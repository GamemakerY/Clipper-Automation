from idea_generator import get_transcript, generate_video_ideas
from video_maker import download_video, crop_video
from final_processing import create_clips, add_captions

def main():
    try:
        video_ID = input("Enter video ID: ")
        get_transcript(video_ID)
        generate_video_ideas(video_ID)
        download_video(video_ID)
        crop_video(video_ID)
        create_clips(video_ID)
        print("All videos generated successfully!")
        
    except Exception as e:
        print(f"An Error Occured: {type(e).__name__}")
        print(f"Error Message: {e}")
        input("")

if __name__ == "__main__":
    main()