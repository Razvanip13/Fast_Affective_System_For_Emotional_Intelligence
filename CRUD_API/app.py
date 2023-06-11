from fastapi import status
from fastapi import Depends, FastAPI, HTTPException
from repository.database import  get_session
from domain.models import *
from typing import List
from sqlmodel import Session
from sqlmodel.sql.expression import Select, SelectOfScalar
from service.service import Service
from fastapi.middleware.cors import CORSMiddleware
import requests

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


@app.get('/users', response_model=List[UserRead], status_code=status.HTTP_200_OK)
async def get_all_users(*, session: Session = Depends(get_session)):
    return serviceEmotions.get_all_users(session)


@app.get('/users/login', status_code=status.HTTP_200_OK)
async def login_user(*, username: str, password: str, session: Session = Depends(get_session)):
    result = serviceEmotions.login_user(username, password, session)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail='The username and password do not match'
        )

    return {
        'key':'YGiLCuTay0SoYQIxh4APS18o/4YlH39wJyKyRtIIO7o=',
        'id':result.id
    }


@app.get('/users/{id}', response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user_by_id(*, id: int, session: Session = Depends(get_session)):
    return serviceEmotions.get_user_by_id(session, id)


@app.get('/tests', response_model=List[TestReadTitle], status_code=status.HTTP_200_OK)
async def get_all_tests(*, limit: int = 10, offset=0, session: Session = Depends(get_session)):
    return serviceEmotions.get_all_tests(session, limit, offset)


@app.get('/tests/{id}', response_model=TestReadContent, status_code=status.HTTP_200_OK)
async def get_test(*, id: int, session: Session = Depends(get_session)):
    return serviceEmotions.get_test(id, session)


@app.get('/emotions', response_model=List[Emotion], status_code=status.HTTP_200_OK)
async def get_all_emotions(*, session: Session = Depends(get_session)):
    return serviceEmotions.get_all_emotions(session)


@app.get('/charts', response_model=List[ChartRead], status_code=status.HTTP_200_OK)
async def get_all_charts(*, session: Session = Depends(get_session)):
    return serviceEmotions.get_all_charts(session)


@app.get('/users/{id_user}/charts', response_model=List[ChartReadTable], status_code=status.HTTP_200_OK)
async def get_charts_for_user(*, id_user: int, session: Session = Depends(get_session)):
    return serviceEmotions.get_charts_for_user(id_user, session)


@app.get('/charts/{id_chart}', response_model=ChartRead, status_code=status.HTTP_200_OK)
async def get_chart(*, id_chart: int, session: Session = Depends(get_session)):
    return serviceEmotions.get_chart(id_chart, session)


@app.get('/captures', response_model=List[CaptureRead], status_code=status.HTTP_200_OK)
async def get_captures(*, session: Session = Depends(get_session)):
    return serviceEmotions.get_captures(session)


@app.get("/users/{idUser}/results",response_model=List[ResultRead],status_code=status.HTTP_200_OK)
async def get_user_results(idUser: int, session: Session = Depends(get_session)):
    return serviceEmotions.get_user_results(idUser, session)


@app.post("/face_emotion")
async def get_face_emotion(face: FaceEmotionRequest):
    result = requests.post("http://localhost:1313/face_emotion",data=face.json())

    return result.json()


@app.post("/voice_emotion")
async def get_voice_emotion(voice: VoiceEmotionRequest):
    result = requests.post("http://localhost:1313/voice_emotion",data=voice.json())

    return result.json()


@app.post("/users/{idUser}/tests/{idTest}/charts/")
async def create_emotional_charts(idUser: int, idTest: int,session: Session = Depends(get_session)):
    result = serviceEmotions.create_charts(idUser, idTest, session)

    return result


@app.post("/results")
async def create_test_result(testSheet: TestSheet, session: Session = Depends(get_session)):
    serviceEmotions.evaluate_test(testSheet, session)
