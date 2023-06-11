import tensorflow as tf
import os
from tensorflow.keras import layers


class FERDenseNet121:

    def __init__(self, model_path) -> None:
        base_model = tf.keras.applications.DenseNet121(
            include_top=False,
            weights="imagenet",
            input_shape=(144, 144, 3),
        )

        for layer in base_model.layers[:14]:
            layer.trainable = False

        x = layers.Flatten()(base_model.output)
        x = layers.Dense(1024, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        predictions = layers.Dense(7, activation='softmax')(x)

        METRICS = [
            'accuracy',
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall')
        ]

        self.__model = tf.keras.Model(inputs=base_model.input, outputs=predictions)
        self.__model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=4e-5),
            loss='categorical_crossentropy',
            metrics=METRICS
        )

        self.__model.load_weights(model_path)

    def predict(self, image):
        return self.__model.predict([image])
