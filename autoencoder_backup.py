import seaborn as sns

import matplotlib.pyplot as plt
from keras.datasets import mnist
import numpy as np

np.random.seed(10)

import numpy as np
from keras.layers import Dense, Input, Dropout
from keras.models import Model
from sklearn.cluster import KMeans
import sklearn.metrics
from sklearn.metrics import confusion_matrix


#extracting data from MNIST
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()
# input numbers you want to use in second arg of np.isin [n,m,x....,h]
train_mask = np.isin(Y_train, [0, 1, 2, 5])
# input numbers you want to use in second arg of np.isin [n,m,x....,h]
test_mask = np.isin(Y_test, [0, 1, 2, 5])
X_train, Y_train = X_train[train_mask], Y_train[train_mask]
X_test, Y_test = X_test[test_mask], Y_test[test_mask]
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255
X_train = X_train.reshape(len(X_train), np.prod(X_train.shape[1:]))
X_test = X_test.reshape(len(X_test), np.prod(X_test.shape[1:]))
# hyper parameters

batch_size = 256
epochs = 200
bottle_dim = 6
# Neural net
########################################################################################################################
#Input layer
input_img = Input(shape=(784,))
# architecture
encoded = Dense(units=500, activation='relu')(input_img)
encoded = Dense(units=500, activation='relu')(encoded)
encoded = Dense(units=2000, activation='relu')(encoded)
encoded = Dense(units=bottle_dim, activation='linear')(encoded)

decoded = Dense(units=2000, activation='relu')(encoded)
decoded = Dense(units=500, activation='relu')(decoded)
decoded = Dense(units=500, activation='relu')(decoded)
# output layer
decoded = Dense(units=784, activation='sigmoid')(decoded)
##################################################################################################################
autoencoder = Model(input_img, decoded)

encoder = Model(input_img, encoded)

autoencoder.summary()

encoder.summary()

autoencoder.compile(optimizer='adam', loss='MSE', metrics=['accuracy'])
history = autoencoder.fit(X_train, X_train,
                          epochs=epochs,
                          batch_size=batch_size,
                          shuffle=True,
                          validation_data=(X_test, X_test))





# summarize history for loss
def loss_plot():
	print(history)
	plt.plot(history.history['loss'])

	plt.title('model loss')
	plt.ylabel('loss')
	plt.xlabel('epoch')
	plt.legend(['train loss'], loc='upper left')
	plt.show(block=False)
loss_plot()



#Clustering
def clustering():
	encoded_imgs_train = encoder.predict(X_test)
	kmeans = KMeans(n_clusters=4, n_init=4000).fit(encoded_imgs_train)
	y_pred_kmeans = kmeans.predict(encoded_imgs_train)
	#Scoring
	score = sklearn.metrics.rand_score(Y_test, y_pred_kmeans)
	print("score is: ", score)

clustering()


# Plots the figueres
def plot_numbers():
	# Prepeares the images for plotting and clustering
	encoded_imgs = encoder.predict(X_test)
	predicted = autoencoder.predict(X_test)
	plt.figure(figsize=(80, 4))
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