from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path

app = FastAPI()

@app.post("/upload-mp3")
async def create_upload_file(file: UploadFile):
    try:
        # Define the folder where the file will be saved
        upload_dir = Path("uploads")

        # Ensure that the parent directory exsits
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Construct the full path for the file
        file_path = upload_dir / file.filename

        # Open the file and save it
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"info": f"file '{file.filename}' saved at '{file_path}'"}
    
    # If there is an error, return an error message
    except Exception as e:
        return {"message": str(e)}
