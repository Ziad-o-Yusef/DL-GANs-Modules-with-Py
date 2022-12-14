# -*- coding: utf-8 -*-
"""Basic _GANs_Model_Python.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_peaBPuqAOQn_9tpB1Ki_GP-iQD3NJwM
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import math 
from tqdm import tqdm

class BasicGANsModel():

  def __init__(self,X_data,random_dim):
    self.X = X_data
    self.random_dim = random_dim


  def handiled_data(self):
    X = (self.X.astype(np.float32) - 127.5)/127.5
    image_dim = X.shape[1]*X.shape[2]*1
    X = X.reshape(253,128*128 )
    random_dim = self.random_dim 
    return X,image_dim,random_dim


  def get_generator(self):
    _,image_dim,random_dim = self.handiled_data()
    gen = tf.keras.Sequential()
    gen.add(tf.keras.layers.Dense(265,input_dim = random_dim))
    gen.add(tf.keras.layers.LeakyReLU(0.2))
    gen.add(tf.keras.layers.Dense(512))
    gen.add(tf.keras.layers.LeakyReLU(0.2))
    gen.add(tf.keras.layers.Dense(1024))
    gen.add(tf.keras.layers.LeakyReLU(0.2))
    gen.add(tf.keras.layers.Dense(image_dim , activation='tanh'))
    gen.compile(loss='binary_crossentropy', optimizer='rmsprop')
    return gen 

  def get_discriminator(self):
    _,image_dim,_ = self.handiled_data()
    disc = tf.keras.Sequential()
    disc.add(tf.keras.layers.Dense(1024, input_dim=image_dim))
    disc.add(tf.keras.layers.LeakyReLU(0.2))
    disc.add(tf.keras.layers.Dropout(0.3))
    disc.add(tf.keras.layers.Dense(512))
    disc.add(tf.keras.layers.LeakyReLU(0.2))
    disc.add(tf.keras.layers.Dropout(0.3))
    disc.add(tf.keras.layers.Dense(256))
    disc.add(tf.keras.layers.LeakyReLU(0.2))
    disc.add(tf.keras.layers.Dropout(0.3))
    disc.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    disc.compile(loss='binary_crossentropy', optimizer='rmsprop')  
    return disc


  def get_gan_network(self,disc,gen):
    _,_,random_dim = self.handiled_data()
    disc.trainable = False
    gan_input = tf.keras.layers.Input(shape=(random_dim))
    x = gen(gan_input)
    gan_output = disc(x)
    gan = tf.keras.models.Model(inputs=gan_input, outputs=gan_output)
    gan.compile(loss='binary_crossentropy', optimizer='adam')
    return gan


  def plot_generated_images(self,epoch, generator, examples=8*8, dim=(8, 8), figsize=(10, 10)):
    _,image_dim,random_dim = self.handiled_data()
    noise = np.random.normal(0, 1, size=[examples, random_dim])
    generated_images = generator.predict(noise)
    generated_images = generated_images.reshape(examples, int(math.sqrt(image_dim)), int(math.sqrt(image_dim)))
    print("==========================================================================================================")
    plt.figure(figsize=figsize)
    for i in range(generated_images.shape[0]):
        plt.subplot(dim[0], dim[1], i+1)
        plt.imshow(generated_images[i], interpolation='nearest', cmap='gray_r')
        plt.axis('off')
    plt.tight_layout()
    plt.savefig('gan_generated_image_epoch_%d.png' % epoch)




  def training(self,epochs = 5, batch_size = 128):

    X,image_dim,random_dim = self.handiled_data()

    batch_count = X.shape[0] / batch_size

    generator = self.get_generator()
    discriminator = self.get_discriminator()
    gan = self.get_gan_network(discriminator,generator)

    for epoch in range(1, epochs+1):
      print('-'*25, 'Epoch %d' % epoch, '-'*25)

      for _ in tqdm(range(int(batch_count))):
        noise = np.random.normal(0, 1, size=[batch_size, random_dim])
        image_batch = X[np.random.randint(0, X.shape[0], size=batch_size)]

        generated_images = generator.predict(noise)
        concat = np.concatenate([image_batch, generated_images])

        y_dis = np.zeros(2*batch_size)
        y_dis[:batch_size] = 0.9

        discriminator.trainable = True
        discriminator.train_on_batch(concat, y_dis)

        noise = np.random.normal(0, 1, size=[batch_size, random_dim])
        y_gen = np.ones(batch_size)
        discriminator.trainable = False
        gan.train_on_batch(noise, y_gen)
        if epoch == 1 or epoch % 20 == 0:
            self.plot_generated_images(epoch, generator)




  def how_to_work(self):
    print(
        '''
        1- Create Object from BasicGANsModel()
        2- set your X dataset (Images) & dim for the generated image in your instance 
        3- call training func() and set  => num of epchs (defult = 10) , => batch size (defult = 128)
        notes : 
        - your dataset should be grayscle 
        - your images should be same & equality size - like (28,28,1)
        THANK YOU :D
        '''
    )

