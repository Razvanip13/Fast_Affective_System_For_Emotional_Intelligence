import os
from tensorflow.keras.models import load_model
from service.voice_emotion_recognotion.AudioPreprocess import AudioPreprocess
import cv2
import threading
from utils.AIUtils import AIUtils


class VoiceEmotionDetector:

    def __init__(self):
        self.__model = load_model(os.path.join(os.getcwd(),'service', 'trained_models','speech_emotion_recognition', 'vgg_transfer_5.h5'))
        self.__audioPreprocessor = AudioPreprocess()
        self.__temp_wav_file_path = os.path.join(os.getcwd(),'interceptor','post_audios','temp.wav')
        self.__label_to_id = {'neutral': 0, 'calm': 1, 'happy': 2, 'sad': 3,'angry': 4, 'fear': 5, 'disgust': 6, 'surprise': 7}
        self.__id_to_label = {0: 'neutral', 1: 'calm', 2: 'happy', 3: 'sad', 4: 'angry', 5: 'fear', 6: 'disgust', 7: 'surprise'}
        self.__fer_label_to_id = {'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3, 'neutral': 4, 'sad': 5, 'surprise': 6, 'calm': 7}

    def __save_last_spectogram(self, image):
        cv2.imwrite(os.path.join(os.getcwd(), 'interceptor', 'post_audios', 'last_spectogram.jpg'), image)

    def get_emotion(self,base64_str):
        self.__audioPreprocessor.generate_temporary_wav_file(base64_str)
        spectrogramImage = self.__audioPreprocessor.get_spectogram(self.__temp_wav_file_path)

        save_thread = threading.Thread(target=self.__save_last_spectogram, args=(spectrogramImage,))
        save_thread.start()

        image = AIUtils.expand_dimensions(image=spectrogramImage)
        soft_values = self.__model.predict(image)[0]
        value, confidence = AIUtils.detect_max_soft_value(soft_values)
        detected_label = self.__id_to_label[value]
        soft_emotions = AIUtils.build_soft_emotions_json(soft_values)

        save_thread.join()

        return {
            'id': self.__fer_label_to_id[detected_label],
            'label': detected_label,
            'confidence': confidence,
            'all_emotions': soft_emotions,
            'proof': base64_str
        }
