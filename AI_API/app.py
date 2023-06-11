from fastapi import Depends, FastAPI
from repository.database import  get_session
from domain.models import *
from sqlmodel import Session
from sqlmodel.sql.expression import Select, SelectOfScalar
from service.service import Service
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

app = FastAPI()
serviceEmotions = Service()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/face_emotion")
async def get_face_emotion(face: FaceEmotionRequest, session: Session = Depends(get_session)):
    result = serviceEmotions.get_face_emotion(face.idChart, face.base64, session)

    if result is None:
        return {"message": "No face found"}

    return {"message": 'Face found'}


@app.post("/voice_emotion")
async def get_voice_emotion(voice: VoiceEmotionRequest, session: Session = Depends(get_session)):
    result = serviceEmotions.get_voice_emotion(voice.idChart, voice.base64, session)

    if result is None:
        return {"message": "No voice found"}

    return {"message": result}


if __name__=="__main__":
    uvicorn.run("app:app", port=1313, reload=True)
