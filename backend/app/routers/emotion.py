import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.emotion_model.emotion_model.emotion_model import EmotionModel
from app.emotion_model.emotion_model.face_preprocessing import FacePreprocessor

router = APIRouter(
    tags=["Emotion"],
    prefix="/emotion",
)

MODEL_PATH = "app/emotion_model/emotion_model/cnn_full_model.pth"
emotion_model = EmotionModel(MODEL_PATH)
face_preprocessor = FacePreprocessor()

latest_emotion = "neutral"  # Variable to store latest detected emotion

def read_image_as_numpy(file: UploadFile) -> np.ndarray:
    file.file.seek(0)  # Reset file pointer
    image_bytes = file.file.read()
    
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image format or corrupted image data.")

    return image

@router.post("/")
async def detect_emotion(files: list[UploadFile] = File(...)):
    global latest_emotion  # Allow modification of the global variable

    if len(files) != 10:
        raise HTTPException(status_code=422, detail="Exactly 10 images are required.")

    frames = []
    for file in files:
        try:
            frame = read_image_as_numpy(file)
            face, bbox = face_preprocessor.preprocess_face(frame)

            if face is None:
                print("No face detected in one of the frames!")
                continue  # Skip this frame instead of failing

            frames.append(face)
        except HTTPException as e:
            return {"error": str(e.detail)}

    if len(frames) == 0:
        raise HTTPException(status_code=400, detail="No faces detected in any of the images.")

    detected_emotions = emotion_model.predict_emotions_from_frames(frames)
    final_emotion = emotion_model.filter_and_select_emotion(detected_emotions)

    latest_emotion = final_emotion  # Store latest detected emotion globally

    return {"detected_emotions": detected_emotions, "final_emotion": final_emotion}

@router.get("/")
async def get_latest_emotion():
    """New GET route to retrieve the latest detected emotion"""
    return {"final_emotion": latest_emotion}
