# -*- coding: utf-8 -*-
"""DCGAN_Module.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kbZjM5ERt0b9LbLB9ax63ztkphPqtSKv
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2 
import os 
import tensorflow as tf
import math 
from tqdm import tqdm 
from tensorflow.keras.layers import Dense,Reshape,Dropout,LeakyReLU,Flatten,BatchNormalization,Conv2D,Conv2DTranspose
from tensorflow.keras.models import Sequential

class DCGAN():
  def __init__(X):
   self.X = X
   np.random.seed(42)
   tf.random.set_seed(42)
   self.random_dim = 100
   self.image_dim = 128*128*1

  def get_generator():    
    generator = Sequential()
    generator.add(Dense(64* 64 * 128, input_shape=[self.random_dim]))
    generator.add(Reshape([64, 64, 128]))
    generator.add(BatchNormalization())
    generator.add(Conv2DTranspose(64, kernel_size=2, strides=2, padding="same",
                                    activation="relu"))
    generator.add(BatchNormalization())
    generator.add(Conv2DTranspose(1, kernel_size=5, strides=1, padding="same",
                                    activation="tanh"))
    generator.compile(loss="binary_crossentropy", optimizer="adam")
    return generator

  def get_discriminator():    
    discriminator = Sequential()
    discriminator.add(Conv2D(64, kernel_size=5, strides=2, padding="same",
                            activation=LeakyReLU(0.3),
                            input_shape=[128,128,1]))
    discriminator.add(Dropout(0.5))
    discriminator.add(Conv2D(128, kernel_size=5, strides=2, padding="same",
                            activation=LeakyReLU(0.3)))
    discriminator.add(Dropout(0.5))
    discriminator.add(Flatten())
    discriminator.add(Dense(1, activation="sigmoid"))
    discriminator.compile(loss="binary_crossentropy", optimizer="adam")
    return discriminator 

  def get_gan_network(disc,gen):
    disc.trainable = False
    gan_input = tf.keras.layers.Input(shape=(self.random_dim))
    x = gen(gan_input)
    gan_output = disc(x)
    gan = tf.keras.models.Model(inputs=gan_input, outputs=gan_output)
    gan.compile(loss='binary_crossentropy', optimizer='adam')
    return gan  
  







  def training(epochs = 5, batch_size = 128):

    batch_count = self.X.shape[0] / batch_size

    generator = self.get_generator()
    discriminator = self.get_discriminator()
    gan = self.get_gan_network(discriminator,generator)

    for epoch in range(1, epochs+1):
      print('-'*25, 'Epoch %d' % epoch, '-'*25)

      for _ in tqdm(range(int(batch_count))):
        noise = np.random.normal(0, 1, size=[batch_size, self.random_dim])
        image_batch = self.X[np.random.randint(0, self.X.shape[0], size=batch_size)]

        generated_images = generator.predict(noise)
        concat = np.concatenate([image_batch, generated_images])

        y_dis = np.zeros(2*batch_size)
        y_dis[:batch_size] = 0.9

        discriminator.trainable = True
        discriminator.train_on_batch(concat, y_dis)

        noise = np.random.normal(0, 1, size=[batch_size, self.random_dim])
        y_gen = np.ones(batch_size)
        discriminator.trainable = False
        gan.train_on_batch(noise, y_gen)
        if epoch == 1 or epoch % 20 == 0:
          self.plot_generated_images(epoch, generator)

  def plot_generated_images(epoch, generator, examples=36, dim=(6, 6), figsize=(6, 6)):
    noise = np.random.normal(0, 1, size=[examples, self.random_dim])
    generated_images = generator.predict(noise)
    generated_images = generated_images.reshape(examples, int(math.sqrt(self.image_dim)),int(math.sqrt(self.image_dim)))
    plt.figure(figsize=figsize)
    for i in range(generated_images.shape[0]):
        plt.subplot(dim[0], dim[1], i+1)
        plt.imshow(generated_images[i], interpolation='nearest', cmap='gray_r')
        plt.axis('off')
    plt.tight_layout()
    plt.savefig('gan_generated_image_epoch_%d.png' % epoch)