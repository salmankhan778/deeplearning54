# -*- coding: utf-8 -*-
"""lab 1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tJX4KSg5p1x9X5nWKodQfBMvZnl8XMnM
"""

!pip install h5py

import h5py

import numpy as np

import h5py
from google.colab import drive
drive.mount('/content/drive')

# Load the file and print the available keys
with h5py.File('/content/drive/MyDrive/Train.h5', 'r') as train_dataset:
    print("Keys in Train.h5:", list(train_dataset.keys()))

with h5py.File('/content/drive/MyDrive/Test.h5', 'r') as test_dataset:
    print("Keys in Test.h5:", list(test_dataset.keys()))

import h5py
import numpy as np
from google.colab import drive

# Mount Google Drive (if not already mounted)
drive.mount('/content/drive', force_remount=True)

# Load the training and test data
with h5py.File('/content/drive/MyDrive/Train.h5', 'r') as train_dataset:
    train_images = np.array(train_dataset['images'][:])
    train_labels = np.array(train_dataset['labels'][:])

with h5py.File('/content/drive/MyDrive/Test.h5', 'r') as test_dataset:
    test_images = np.array(test_dataset['images'][:])
    test_labels = np.array(test_dataset['labels'][:])

print("Training and test data loaded successfully.")

# Flatten and normalize the images
train_images = train_images.reshape(train_images.shape[0], -1) / 255.0
test_images = test_images.reshape(test_images.shape[0], -1) / 255.0

# Convert labels to one-hot encoding
num_classes = len(np.unique(train_labels))
train_labels_one_hot = np.eye(num_classes)[train_labels]
test_labels_one_hot = np.eye(num_classes)[test_labels]

print("Data preprocessing completed.")

def softmax(z):
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # for numerical stability
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

def compute_cost(y_true, y_pred):
    m = y_true.shape[0]
    return -np.sum(y_true * np.log(y_pred + 1e-8)) / m  # adding epsilon for numerical stability

"""4. Gradient Descent


"""

def gradient_descent(X, y, weights, bias, learning_rate):
    m = X.shape[0]

    # Forward propagation
    z = np.dot(X, weights) + bias
    y_pred = softmax(z)

    # Compute gradients
    dz = y_pred - y
    dw = np.dot(X.T, dz) / m
    db = np.sum(dz) / m

    # Update parameters
    weights -= learning_rate * dw
    bias -= learning_rate * db

    return weights, bias

"""## 5. Model **Training**




"""

# Initialize parameters
num_features = train_images.shape[1]
weights = np.random.randn(num_features, num_classes) * 0.01
bias = np.zeros((1, num_classes))

# Training parameters
learning_rate = 0.1
num_epochs = 1000

# Training loop
for epoch in range(num_epochs):
    # Update weights and bias using gradient descent
    weights, bias = gradient_descent(train_images, train_labels_one_hot, weights, bias, learning_rate)

    # Calculate cost every 100 epochs
    if epoch % 100 == 0:
        z = np.dot(train_images, weights) + bias
        y_pred = softmax(z)
        cost = compute_cost(train_labels_one_hot, y_pred)
        print(f"Epoch {epoch}, Cost: {cost}")

# Function to make predictions
def predict(X, weights, bias):
    z = np.dot(X, weights) + bias
    y_pred = softmax(z)
    return np.argmax(y_pred, axis=1)

# Predictions on test set
test_predictions = predict(test_images, weights, bias)

# Calculate accuracy
accuracy = np.mean(test_predictions == test_labels) * 100
print(f"Test Set Accuracy: {accuracy:.2f}%")