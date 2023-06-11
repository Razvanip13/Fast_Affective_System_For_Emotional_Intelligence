import numpy as np


class AIUtils:
    def __init__(self):
        pass

    @staticmethod
    def detect_max_soft_value(soft_values):
        maxim = soft_values[0]
        current = 0
        for j in range(1, len(soft_values)):
            if soft_values[j] > maxim:
                current = j
                maxim = soft_values[j]

        return current,maxim

    @staticmethod
    def build_soft_emotions_json(soft_values):
        return {
            'angry': soft_values[0],
            'disgust': soft_values[1],
            'fear': soft_values[2],
            'happy': soft_values[3],
            'neutral': soft_values[4],
            'sad': soft_values[5],
            'surprise': soft_values[6]
        }

    @staticmethod
    def expand_dimensions(image):
        return np.expand_dims(image, axis=0)
