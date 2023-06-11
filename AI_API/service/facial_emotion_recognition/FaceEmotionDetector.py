import base64

import numpy as np
from service.facial_emotion_recognition.FERDenseNet121 import FERDenseNet121
import cv2
import os
import threading
from service.facial_emotion_recognition.FacePreprocess import FacePreprocess
from utils.AIUtils import AIUtils


class FaceEmotionDetector:

    def __init__(self, ) -> None:
        self.__model = FERDenseNet121(
            os.path.join(
                os.getcwd(), "service", 'trained_models', "facial_emotion_recognition", 'DenseNet121FEREQCUBIC2.h5'
            )
        )
        self.__fer_label_to_id = {
            'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3, 'neutral': 4, 'sad': 5, 'surprise': 6
        }
        self.__fer_id_to_label = {
            0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'
        }

        self.__facePreprocess = FacePreprocess()

    def __detect_label(self, soft_values):

        value, confidence = AIUtils.detect_max_soft_value(soft_values)
        detected_label = self.__fer_id_to_label[value]
        soft_emotions = AIUtils.build_soft_emotions_json(soft_values)

        return {'id': value, 'label': detected_label, 'confidence': confidence, 'all_emotions': soft_emotions}

    def __save_last_image(self, image):
        cv2.imwrite(os.path.join(os.getcwd(), 'interceptor', 'post_images', 'last_image.jpg'), image)

    def get_emotion(self, base64_str):
        currentFrame = self.__facePreprocess.decode_base64(base64_str)

        if currentFrame is None:
            return None

        currentFrameInBW = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY)
        faces = self.__facePreprocess.locate_faces(currentFrameInBW)

        if len(faces[0]) == 0:
            return None

        img = self.__facePreprocess.select_highest_confidence_face(faces,currentFrameInBW)
        image_preprocessed = self.__facePreprocess.get_image_equalized_bicubic(image=img)
        squeezed_image = np.squeeze(image_preprocessed)

        save_thread = threading.Thread(target=self.__save_last_image, args=(squeezed_image,))

        save_thread.start()
        answer = self.__detect_label(self.__model.predict([image_preprocessed / 255.0])[0])
        save_thread.join()

        with open("interceptor\post_images\last_image.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        answer['proof'] = encoded_string

        return answer
