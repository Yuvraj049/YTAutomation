import os
import subprocess
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# OAuth2 Scopes for YouTube API
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Function to authenticate and get the API client
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json', SCOPES)

    credentials = flow.run_local_server(port=3000)
    return build('youtube', 'v3', credentials=credentials)

def run_description_generator(video_title):
    # Assuming the description generator is a script called `description_generator.py`
    # and it accepts the video title as an argument and returns the description
    try:
        # Running the external app and capturing its output
        result = subprocess.run(['python', 'description_generator.py', video_title],
                                capture_output=True, text=True, check=True)
        
        # The description is expected to be in stdout
        description = result.stdout.strip()  # Stripping any extra whitespace or newlines
        return description

    except subprocess.CalledProcessError as e:
        print(f"Error running description generator: {e}")
        return f"Default description for {video_title}"  # Fallback if the generator fails
    
# Function to upload video
def upload_video(youtube, video_path, video_title, video_description):

    video_description = run_description_generator(video_title)
    video_description+=" #shorts #JoeRogan #JoeRoganExperience #JRE #podcast"
    print(video_description)
    body = {
        'snippet': {
            'title': video_title,
            'description': video_description,
            'tags': ['video', 'upload'],
            'categoryId': '22'  # This is the YouTube category ID for "People & Blogs"
        },
        'status': {
            'privacyStatus': 'public',  # Set it to "private" or "unlisted" if needed
            'madeForKids': True  # Mark the video as "Made for Kids"
        }
    }

    # Uploading the video
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/*')
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Video {video_title} uploaded successfully.")
    return response

# Main function to scan a folder and upload all videos
def upload_videos_from_folder(folder_path):
    youtube = get_authenticated_service()
    for filename in os.listdir(folder_path):
        if filename.endswith(('.mp4', '.mov', '.avi', '.mkv')):
            video_path = os.path.join(folder_path, filename)
            video_title = os.path.splitext(filename)[0]  # Video title is the filename without extension
            video_description = video_title  # Using the title as description
            print(f"Uploading {filename}...")
            upload_video(youtube, video_path, video_title, video_description)

if __name__ == '__main__':
    folder_path = './media'  # Replace with the actual folder path
    upload_videos_from_folder(folder_path)
