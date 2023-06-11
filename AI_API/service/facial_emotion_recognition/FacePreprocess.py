import numpy as np
import cv2
import os
import base64


class FacePreprocess:

    def __init__(self):
        self.__haarCascadeClassifier = cv2.CascadeClassifier(
            os.path.join(
                os.getcwd(), "service", "trained_models", "face_detection", "haarcascade_frontalface_default.xml"
            )
        )

    def get_image_equalized_bicubic(self, image):
        img_resized = np.copy(image)

        if image.shape[0] != 144 or image.shape[1] != 144:
            img_resized = cv2.resize(
                image,
                None,
                fx=144 / image.shape[0],
                fy=144 / image.shape[1],
                interpolation=cv2.INTER_CUBIC
            )

        equ = cv2.equalizeHist(img_resized)
        stacked_image = np.stack((equ,) * 3, axis=-1)
        img = np.expand_dims(stacked_image, axis=0)

        return img

    def decode_base64(self,base64_str):
        encoded_data = base64_str.split(',')
        if len(encoded_data) > 1:
            encoded_data = encoded_data[1]
        else:
            encoded_data = encoded_data[0]

        decoded_data = base64.b64decode(encoded_data)
        np_data = np.fromstring(decoded_data, np.uint8)
        currentFrame = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

        return currentFrame

    def locate_faces(self,currentFrameInBW):
        faces = self.__haarCascadeClassifier.detectMultiScale3(
            currentFrameInBW,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
            outputRejectLevels=True
        )

        return faces

    def select_highest_confidence_face(self,faces,currentFrameInBW):
        rects = faces[0]
        weights = faces[2]

        max_confidence_face = rects[0]
        the_weights = weights.tolist()
        max_confidence = the_weights[0]
        for i in range(1, len(weights)):
            if max_confidence < the_weights[i]:
                max_confidence = the_weights[i]
                max_confidence_face = rects[i]

        xCoord = max_confidence_face[0]
        yCoord = max_confidence_face[1]
        width = max_confidence_face[2]
        height = max_confidence_face[3]

        img = currentFrameInBW[yCoord:yCoord + height, xCoord:xCoord + width]

        return img
