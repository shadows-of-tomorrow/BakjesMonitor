import numpy as np
import tensorflow as tf
import pandas as pd

# 1. Load MNIST handwritten digit data.
digits = np.genfromtxt("D:/alu-robo/digits/csv28/digits.csv", delimiter=',')
X_train, y_train = digits[:, 1:], digits[:, 0]

# 2. Reshape image pixels and one-hot encode labels.
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype('float32') / 255.0
y_train = pd.get_dummies(pd.Series(y_train))

# 3. Build convolutional neural network architecture.
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(100, activation='relu', kernel_initializer='he_uniform'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))

# 4. Compile model using cross-entropy loss.
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 5. Fit model parameters.
model.fit(x=X_train, y=y_train, epochs=5)

# 6. Store model.
model.save("./models/digits_nn")
