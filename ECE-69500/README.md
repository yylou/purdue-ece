# Deep Learning

<br />

## 1. Torchvision and Random Tensors
> (1) How to extract pixels from images  
  (2) How to augment your training data by applying various kinds of transformations to the data you start out with  
  (3) How to generate random tensors since that can be a useful thing to do when you are testing your code

### Images Representations
* Tensor of shape ```(C, H, W)```
* Numpy ```(H, W, C)```
* Feed into the neural network ```(B, C, H, W)```
* PIL object

### Scaling and Normalization
* Scale [0, 255] to [0, +1.0] ```torchvision.transforms.ToTensor```
* Transform [0, +1.0] to [-1.0, +1.0] ```torchvision.transforms.Normalize```