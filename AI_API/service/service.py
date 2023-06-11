from domain.models import Capture
from sqlmodel import Session
from service.facial_emotion_recognition.FaceEmotionDetector import FaceEmotionDetector
from service.voice_emotion_recognotion.VoiceEmotionDetector import VoiceEmotionDetector


class Service:

    def __init__(self):
        self.__faceModel = FaceEmotionDetector()
        self.__voiceModel = VoiceEmotionDetector()


    def get_face_emotion(self, idChart: int, face: str, session: Session):
        result = self.__faceModel.get_emotion(face)

        if result is None:
            return None

        capture = Capture(
            idChart=str(idChart),
            idEmotion=str(result['id'] + 1),
            confidence=result['confidence'],
            angry=result['all_emotions']['angry'],
            disgust=result['all_emotions']['disgust'],
            fear=result['all_emotions']['fear'],
            happy=result['all_emotions']['happy'],
            neutral=result['all_emotions']['neutral'],
            sad=result['all_emotions']['sad'],
            surprise=result['all_emotions']['surprise'],
            proof=result['proof']
        )

        session.add(capture)
        session.commit()

        return result

    def get_voice_emotion(self, idChart: int, voice: str, session: Session):
        result = self.__voiceModel.get_emotion(voice)

        capture = Capture(
            idChart=str(idChart),
            idEmotion=str(result['id'] + 1),
            confidence=result['confidence'],
            angry=result['all_emotions']['angry'],
            disgust=result['all_emotions']['disgust'],
            fear=result['all_emotions']['fear'],
            happy=result['all_emotions']['happy'],
            neutral=result['all_emotions']['neutral'],
            sad=result['all_emotions']['sad'],
            surprise=result['all_emotions']['surprise'],
            proof = result['proof']
        )

        session.add(capture)
        session.commit()

        return result['label']

