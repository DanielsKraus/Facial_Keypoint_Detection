## TODO: define the convolutional neural network architecture

import torch
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I

L1_IN = 1
L1_OUT = 32
L2_OUT = L1_OUT * 2
L3_OUT = L2_OUT * 2
L4_OUT = L3_OUT * 2
FLATTEN = L4_OUT*12*12
FC = 1000
KP = 68 * 2


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or             batch normalization) to avoid overfitting
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        
        # Covolutional Layers
        self.conv1 = nn.Conv2d(L1_IN,L1_OUT,5)
        self.conv2 = nn.Conv2d(L1_OUT,L2_OUT,3)
        self.conv3 = nn.Conv2d(L2_OUT,L3_OUT,3)
        self.conv4 = nn.Conv2d(L3_OUT,L4_OUT,2)

        # Maxpooling Layer
        self.pool = nn.MaxPool2d(2,2)

        # Fully Connected Layers
        self.fc1 = nn.Linear(FLATTEN,FC) 
        self.fc2 = nn.Linear(FC,FC)
        self.fc3 = nn.Linear(FC,KP) 

        # Dropouts
        self.drop1 = nn.Dropout(0.1)
        self.drop2 = nn.Dropout(0.2)
        self.drop3 = nn.Dropout(0.3)
        self.drop4 = nn.Dropout(0.4)
        self.drop5 = nn.Dropout(0.5)
        self.drop6 = nn.Dropout(0.6)     

        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        ## x = self.pool(F.relu(self.conv1(x)))
        x = self.drop1(self.pool(F.relu(self.conv1(x))))
        #print("First size: ", x.shape)
        # Second - Convolution + Activation + Pooling + Dropout
        x = self.drop2(self.pool(F.relu(self.conv2(x))))
        #print("Second size: ", x.shape)
        # Third - Convolution + Activation + Pooling + Dropout
        x = self.drop3(self.pool(F.relu(self.conv3(x))))
        #print("Third size: ", x.shape)
        # Forth - Convolution + Activation + Pooling + Dropout
        x = self.drop4(self.pool(F.relu(self.conv4(x))))
        #print("Forth size: ", x.shape)
        # Flattening the layer
        x = x.view(x.size(0), -1)
        #print("Flatten size: ", x.shape)
        # First - Dense + Activation + Dropout
        x = self.drop5(F.relu(self.fc1(x)))
        #print("First dense size: ", x.shape)
        # Second - Dense + Activation + Dropout
        x = self.drop6(F.relu(self.fc2(x)))
        # a modified x, having gone through all the layers of your model, should be returned
        # Final Dense Layer
        return self.fc3(x)
        