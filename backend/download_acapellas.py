import pandas as pd
from pytubefix import YouTube
from pathlib import Path
import os
from pydub import AudioSegment
import re

# Define the path to the CSV file and where to store downloaded files
csv_file_name = Path('datasets/real_acapellas.csv')
upload_dir = Path("datasets/real_vocals")

# Ensure that the parent directory exsits
upload_dir.mkdir(parents=True, exist_ok=True)

# Function to sanitize filename by removing unwanted characters
def sanitize_filename(name):
    return re.sub(r'[\\/:"*?<>|!]', '', name)

# Function to download audio from a YouTube link and trim it with init and fin
def download_audio(url, filename, init, fin):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        
        # Download the audio file
        video_path_str = video.download(output_path=str(upload_dir))
        
        # Load the downloaded audio file
        audio = AudioSegment.from_file(video_path_str)
        
        # Convert init and fin to milliseconds
        start_time = init * 1000  # pydub works in milliseconds
        end_time = fin * 1000 if fin else len(audio)  # if no fin, use full length
        
        # Trim the audio to the specified section
        trimmed_audio = audio[start_time:end_time]
        
        # Construct final file path with .mp3 extension
        final_file_path = upload_dir / (sanitize_filename(filename))
        trimmed_audio.export(final_file_path, format="mp3")
        
        # Remove the original download
        os.remove(video_path_str)
        
        print(f"Downloaded and saved as .mp3: {final_file_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Load CSV and iterate through rows
df = pd.read_csv(csv_file_name)
filtered_file = df.loc[:, ['Init', 'Fin', 'Song Name', 'Link']]

# Download each audio file using the YouTube link
for index, row in filtered_file.iterrows():
    url = row.get('Link') # link to the youtube video
    init = row.get('Init') # where to start the video from
    fin = row.get('Fin') # where to end the video
    song_name = row.get('Song Name')

    # Construct the filename using init and fin values
    filename = f"{song_name}.mp3"
    if url:
        # Ensure the URL starts with 'https://'
        if not url.startswith('https://'):
            url = f"https://{url}"
        download_audio(f"{url}", filename, init, fin)
