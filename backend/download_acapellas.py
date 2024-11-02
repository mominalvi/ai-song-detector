import pandas as pd
from pytubefix import YouTube
from pathlib import Path
import os

# Define the path to the CSV file and where to store downloaded files
csv_file_name = 'real_acapellas.csv'
upload_dir = Path("datasets")

# Ensure that the parent directory exsits
upload_dir.mkdir(parents=True, exist_ok=True)

# Construct the full path for the file
csv_file_path = upload_dir / csv_file_name

# Function to download audio from a YouTube link
def download_audio(url, filename):
    try:
        yt = YouTube(url)

        # extracting audio
        video = yt.streams.filter(only_audio=True).first()
        video_path = video.download(output_path=upload_dir)
        
        # Convert downloaded file to .mp3
        base, ext = os.path.splitext(video_path)
        new_file = base + '.mp3'
        os.rename(video_path, new_file)
        
        print(f"Downloaded and saved: {new_file}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Load CSV and iterate through rows
df = pd.read_csv(csv_file_path)
filtered_file = df.loc[:, ['Init', 'Fin', 'Song Name', 'Link']]

# Download each audio file using the YouTube link
for index, row in filtered_file.iterrows():
    url = row.get('Link') # link to the youtube video
    init = row.get('Init') # where to start the video from
    fin = row.get('Fin') # where to end the video
    song_name = row.get('Song name')

    # Construct the filename using init and fin values
    filename = f"{song_name}.mp3"
    if url:
        download_audio(f"https://{url}", filename)
