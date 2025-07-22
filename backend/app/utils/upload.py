import aiofiles
import os
from fastapi import HTTPException, UploadFile
from datetime import datetime

async def save_upload_file(upload_file: UploadFile, destination_path: str, type:str, file_extension) -> str:
    try:
        post_datetime = datetime.utcnow().strftime("%Y%d%m%H%M%S")
        
        # add current user id later
        filename = type + "_" + post_datetime + file_extension
        file_path = os.path.join(destination_path, filename)

        if os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="File already exists")

        async with aiofiles.open(file_path, "wb") as buffer:
            # Read file content as bytes and write to destination
            content = await upload_file.read()
            await buffer.write(content)

        return file_path

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
