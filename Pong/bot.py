import random

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras import initializers


def build_model():
    activation_types = ['relu', 'sigmoid', 'softplus', 'tanh']
    model = Sequential()
    model.add(Dense(10, kernel_initializer=initializers.RandomUniform(minval=-0.9, maxval=0.9, seed=None),
                    input_dim=6, activation=random.choice(activation_types)))
    model.add(Dense(6, kernel_initializer=initializers.RandomUniform(minval=-0.9, maxval=0.9, seed=None),
                    activation=random.choice(activation_types)))
    model.add(Dense(2, kernel_initializer=initializers.RandomUniform(minval=-0.9, maxval=0.9, seed=None),
                    activation='sigmoid'))
    return model


class PongBot:
    def __init__(self, model=None):
        if model is not None:
            self.model = model
            self.update_model()
        else:
            self.model = build_model()

    def update_model(self):
        initial_weights = self.model.get_weights()
        new_weights = []
        THRESHOLD = 0.7
        MAX_DELT = 0.03
        for i in initial_weights:
            new = random.random()
            if new > THRESHOLD:
                if len(i.shape) > 1:
                    row = random.randrange(0, i.shape[0])
                    column = random.randrange(0, i.shape[1])
                    i[row][column] += (random.random() - 0.5)*MAX_DELT
            new_weights.append(i)
        self.model.set_weights(new_weights)

    def get_move(self, ball, paddle):
        input_list = [ball.x, ball.y, ball.velocity[0], ball.velocity[1], paddle.x, paddle.y]
        input_data = np.asarray(input_list).reshape(1,-1)
        output_list = self.model.predict(input_data)[0]
        if output_list[0] > output_list[1]:
            output_list[0] = round(output_list[0])
            output_list[1] = 0
        else:
            output_list[1] = round(output_list[1])
            output_list[0] = 0
        return output_list

"""
x= PongBot()
test_data = np.random.random((1,6))
print(test_data)
print(x.model.predict(test_data))
x.update_model()
print(x.model.predict(test_data))
"""