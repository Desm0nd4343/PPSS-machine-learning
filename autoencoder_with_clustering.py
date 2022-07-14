from keras.datasets import mnist
from keras.layers import Input, Dense
from keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
import numpy as np

np.random.seed(10)

from time import time
import numpy as np
import keras.backend as K
from tensorflow.python.keras.layers import Layer, InputSpec
from keras.layers import Dense, Input, Dropout
from keras.models import Model
from tensorflow.keras.optimizers import SGD
from keras import callbacks
from keras.initializers import VarianceScaling
from sklearn.cluster import KMeans
import sklearn.metrics

# Loading training data
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255
X_train = X_train.reshape(len(X_train), np.prod(X_train.shape[1:]))
X_test = X_test.reshape(len(X_test), np.prod(X_test.shape[1:]))
print(X_train.shape)
print(X_test.shape)


# hyper parameters
batch_size = 256
epochs = 2
bottle_dim = 10
# Neural net
input_img = Input(shape=(784,))

# architecture
encoded = Dense(units=2000, activation='relu')(input_img)
encoded = Dense(units=256, activation='relu')(encoded)
encoded = Dense(units=256, activation='relu')(encoded)
encoded = Dense(units=256, activation='relu')(encoded)
encoded = Dense(units=256, activation='relu')(encoded)
encoded = Dense(units=bottle_dim, activation='linear')(encoded)

decoded = Dense(units=256, activation='relu')(encoded)
decoded = Dense(units=256, activation='relu')(decoded)
decoded = Dense(units=256, activation='relu')(decoded)
decoded = Dense(units=256, activation='relu')(decoded)
decoded = Dense(units=784, activation='sigmoid')(decoded)

autoencoder = Model(input_img, decoded)

encoder = Model(input_img, encoded)

autoencoder.summary()

encoder.summary()

autoencoder.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = autoencoder.fit(X_train, X_train,
                          epochs=epochs,
                          batch_size=batch_size,
                          shuffle=True,
                          validation_data=(X_test, X_test))


# Prepeares the images for plotting and clustering
encoded_imgs = encoder.predict(X_test)
predicted = autoencoder.predict(X_test)


# summarize history for loss
def loss_plot():
	print(history)
	plt.plot(history.history['loss'])

	plt.title('model loss')
	plt.ylabel('loss')
	plt.xlabel('epoch')
	plt.legend(['train loss'], loc='upper left')
	plt.show(block=False)



#Clustering
def clustering():
	kmeans = KMeans(n_clusters=10, n_init=100)
	y_pred_kmeans = kmeans.fit_predict(encoded_imgs)
	y_pred_kmeans[:10]
	#Scoring
	score = sklearn.metrics.rand_score(Y_test, y_pred_kmeans)
	print(score)
clustering()


# Plots the figueres
def plot_numbers():
	plt.figure(figsize=(40, 4))
	for i in range(10):
		# display original images
		ax = plt.subplot(3, 20, i + 1)
		plt.imshow(X_test[i].reshape(28, 28))
		plt.gray()
		ax.get_xaxis().set_visible(False)
		ax.get_yaxis().set_visible(False)

		# display encoded images
		ax = plt.subplot(3, 20, i + 1 + 20)
		plt.imshow(encoded_imgs[i].reshape(bottle_dim, 1))
		plt.gray()
		ax.get_xaxis().set_visible(False)
		ax.get_yaxis().set_visible(False)

		# display reconstructed images
		ax = plt.subplot(3, 20, 2 * 20 + i + 1)
		plt.imshow(predicted[i].reshape(28, 28))
		plt.gray()
		ax.get_xaxis().set_visible(False)
		ax.get_yaxis().set_visible(False)
	plt.show()
plot_numbers()