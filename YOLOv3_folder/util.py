{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "from __future__ import division\n",
    "\n",
    "import torch \n",
    "import torch.nn as nn\n",
    "import torch.nn.functional as F \n",
    "from torch.autograd import Variable\n",
    "import numpy as np\n",
    "import cv2 "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "def predict_transform(prediction, inp_dim, anchors, num_classes, CUDA = True):\n",
    "\n",
    "    \n",
    "    batch_size = prediction.size(0)\n",
    "    stride =  inp_dim // prediction.size(2)\n",
    "    grid_size = inp_dim // stride\n",
    "    bbox_attrs = 5 + num_classes\n",
    "    num_anchors = len(anchors)\n",
    "    \n",
    "    prediction = prediction.view(batch_size, bbox_attrs*num_anchors, grid_size*grid_size)\n",
    "    prediction = prediction.transpose(1,2).contiguous()\n",
    "    prediction = prediction.view(batch_size, grid_size*grid_size*num_anchors, bbox_attrs)\n",
    "    anchors = [(a[0]/stride, a[1]/stride) for a in anchors]\n",
    "\n",
    "    #Sigmoid the  centre_X, centre_Y. and object confidencce\n",
    "    prediction[:,:,0] = torch.sigmoid(prediction[:,:,0])\n",
    "    prediction[:,:,1] = torch.sigmoid(prediction[:,:,1])\n",
    "    prediction[:,:,4] = torch.sigmoid(prediction[:,:,4])\n",
    "    \n",
    "    #Add the center offsets\n",
    "    grid = np.arange(grid_size)\n",
    "    a,b = np.meshgrid(grid, grid)\n",
    "\n",
    "    x_offset = torch.FloatTensor(a).view(-1,1)\n",
    "    y_offset = torch.FloatTensor(b).view(-1,1)\n",
    "\n",
    "    if CUDA:\n",
    "        x_offset = x_offset.cuda()\n",
    "        y_offset = y_offset.cuda()\n",
    "\n",
    "    x_y_offset = torch.cat((x_offset, y_offset), 1).repeat(1,num_anchors).view(-1,2).unsqueeze(0)\n",
    "\n",
    "    prediction[:,:,:2] += x_y_offset\n",
    "\n",
    "    #log space transform height and the width\n",
    "    anchors = torch.FloatTensor(anchors)\n",
    "\n",
    "    if CUDA:\n",
    "        anchors = anchors.cuda()\n",
    "\n",
    "    anchors = anchors.repeat(grid_size*grid_size, 1).unsqueeze(0)\n",
    "    prediction[:,:,2:4] = torch.exp(prediction[:,:,2:4])*anchors\n",
    "    \n",
    "    prediction[:,:,5: 5 + num_classes] = torch.sigmoid((prediction[:,:, 5 : 5 + num_classes]))\n",
    "\n",
    "    prediction[:,:,:4] *= stride\n",
    "    \n",
    "    return prediction"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
