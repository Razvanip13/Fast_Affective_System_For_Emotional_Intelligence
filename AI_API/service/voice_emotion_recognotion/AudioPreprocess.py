import librosa
import numpy as np
import base64
import os
from pydub import AudioSegment


class AudioPreprocess():
    def __init__(self):
        self.__maxSize = 228

    def __scale_minmax(self, X, min=0.0, max=1.0):
        X_std = (X - X.min()) / (X.max() - X.min())
        X_scaled = X_std * (max - min) + min
        return X_scaled

    def __spectrogram_image(self, y, sr, hop_length, n_mels):
        mels = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels,
                                              n_fft=2*hop_length, hop_length=hop_length)
        mels = np.log(mels + 1e-9)

        img = self.__scale_minmax(mels, 0, 255).astype(np.uint8)
        img = np.flip(img, axis=0)
        img = 255 - img

        return img

    def generate_temporary_wav_file(self, base64_string):
        decode_string = base64.b64decode(base64_string)

        with open(os.path.join(os.getcwd(), 'interceptor','post_audios', "temp.webm"), "wb") as wav_file:
            wav_file.write(decode_string)

        sound = AudioSegment.from_file(os.path.join(os.getcwd(), 'interceptor','post_audios', "temp.webm"))
        sound.export(os.path.join(os.getcwd(), 'interceptor', 'post_audios', 'temp.wav'), format="wav")

    def get_spectogram(self, filename):
        scale, sr = librosa.load(filename)
        scale = librosa.to_mono(scale)
        features = self.__spectrogram_image(scale, sr, 512, 120)
        if features.shape[1] < self.__maxSize:
            features = np.pad(features, [(0, 0), (0, self.__maxSize - features.shape[1])], 'constant', constant_values=255)
        elif features.shape[1] > self.__maxSize:
            features = features[:, :self.__maxSize]

        relax_value = 40
        for i in range(len(features)):
            for j in range(len(features[i])):
                if features[i,j] + relax_value > 255:
                    features[i,j] = 255
                else:
                    features[i,j] = features[i,j] + relax_value

        return np.stack((features,) * 3, axis=-1)
