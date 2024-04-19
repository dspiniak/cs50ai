import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
# categories should be 43
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    print(f"LOADED DATA")

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
	# this should work regardless of operating system (support '/' and '\')
        # for this use os.sep and os.path.join
        # each directory is one category
        # read each image via numpy.ndarray using OpenCV-Python (cv2)
        # resize images so all have the same img_width and img_weight
        # return tuple (images, labels) image arrays and labels for each image in the data set
        # images is a list of images in data set represented as a numpy.ndarray
        # labels should be a list of integers, representing the categoy number for each corresponding image
	

    main_directory = data_dir
    data = set()
    data_tuple = tuple()
    images = list()
    labels = list()
    for label in os.listdir(main_directory):
        label_directory = os.path.join(main_directory, label)
        if os.path.isdir(label_directory):
            for filename in os.listdir(label_directory):
                if filename.endswith('.ppm'):
                    image_path = os.path.join(label_directory,filename)
                    image = cv2.imread(image_path)
                    image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

                    images.append(image)
                    labels.append(label)

    images = np.array(images)            
    data = (images, labels)
    return data


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Create a convolutional neural network
    model = tf.keras.models.Sequential([

        # Convolutional layer. Learn 32 filters using a 3x3 kernel
            # assume input of shape (IMG_WIDTH, IMG_HEIGHT, 3)
                # image of width IMG_WIDTH, height IMG_HEIGHT, and 3 values for each pixel for red, green, and blue
        tf.keras.layers.Conv2D(
            32, (6, 6), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Max-pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # The output layer of the neural network should have NUM_CATEGORIES units, one for each of the traffic sign categories.
        # Add an output layer with output units for all 10 digits
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()
