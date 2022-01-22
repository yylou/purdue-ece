# Deep Learning

<br />

## 1. Torchvision and Random Tensors
> (1) How to extract pixels from images (typical image consists of **RGB color planes** referred to as **channels** in **unsigned 8-bit integer**)  
  (2) How to **augment your training data** by applying various kinds of transformations to the data you start out with  
  (3) How to **generate random tensors** since that can be a useful thing to do when you are testing your code

### Images Representations
* Tensor of shape ```(C, H, W)```
* Numpy ```(H, W, C)```
* Feed into the neural network ```(B, C, H, W)```
* PIL (Python Imaging Library) object ```(W, H)```

```Python
img = Image.open('pic.jpg')
print(img.format, img.size, img.mode)   # JPEG (3024, 4032) RGB
W, H = img.size
print(img.getpixel((100, 150)), '\n')   # (162, 163, 149)

"""
np.array[150, 100, :]       = (H, W, C)
img.getpixel((100, 150))    = (W, H)
torch.array[:, 150, 100]    = (C, H, W)
"""
array = np.zeros((H, W, 3), dtype=np.uint8)
print(array[150, 100, :])               # [0 0 0]
array[150, 100, :] = img.getpixel((100, 150))
print(array[150, 100, :], '\n')         # [162 163 149]

array = torch.zeros(3, H, W, dtype=torch.uint8)
print(array[:, 150, 100])               # tensor([0, 0, 0], dtype=torch.uint8)
array[:, 150, 100] = torch.tensor(img.getpixel((100, 150)))
print(array[:, 150, 100])               # tensor([162, 163, 149], dtype=torch.uint8)
```

<br />

### Scaling, Normalization, Data Augmentation
* Scale [0, 255] to [0, +1.0] ```torchvision.transforms.ToTensor```
* Transform [0, +1.0] to [-1.0, +1.0] ```torchvision.transforms.Normalize```
* Augment training data ```torchvision.transforms```

```Python
"""
Cast to torch.uint8 is very important because of the input datatype requirements of image-facing PyTorch functions
"""
img = torch.randint(0, 256, (1, 1, 3, 3)).type(torch.uint8)  # (batch_size, C, H, W) = (1, 1, 3, 3)
print(img[0], '\n')
"""
tensor([[[228, 255, 166],
            [194, 255, 244],
            [132, 171, 147]]], dtype=torch.uint8)
"""
print(img[0] == img[0, :, :, :], '\n')
"""
tensor([[[True, True, True],
            [True, True, True],
            [True, True, True]]]) 
"""

img = torch.randint(0, 256, (4, 3, 5, 9)).type(torch.uint8)  # (batch_size, C, H, W) = (4, 3, 5, 9)
print(img[0], '\n')
"""
tensor([[[183,  60, 246, 216,   2, 109, 247, 239,  58],
        [ 92, 173, 156,  69,  59, 125,  59, 233, 252],
        [153, 185,  58, 225,  54, 247, 168,  34,  91],
        [139, 164, 134, 122, 178, 186, 187,  78,  53],
        [ 61,  80, 199, 157, 114,  49, 218, 152, 145]],

        [[215, 216, 253,  70,  10,  76, 116, 131, 154],
        [ 88,  74,  57,  86, 159, 238, 247,  78, 161],
        [ 97, 243, 155, 252, 170, 167,  54, 127,  21],
        [242, 169, 224, 134, 234, 146, 210, 213, 241],
        [138, 141, 111, 239, 168, 137, 128,  66,  44]],

        [[226, 234, 172,   5, 252,  79, 192, 119, 157],
        [ 61,  47, 114, 206, 163, 255, 219, 125,  79],
        [154, 102,  67, 198, 185, 189,  15, 108, 149],
        [ 75,   5, 222,  83, 179, 162, 142, 143, 192],
        [ 61, 223,  83, 169,   0,   6, 156,  40,  33]]], dtype=torch.uint8) 
"""

print(img.max())                # tensor(255, dtype=torch.uint8)
max_pixel_position = (img == img.max()).nonzero()
print(max_pixel_position, '\n') # tensor([[0, 2, 1, 5],
                                #         [1, 2, 0, 0],
                                #         [2, 1, 0, 2]])

print(img.min())                # tensor(0, dtype=torch.uint8)
min_pixel_position = (img == img.min()).nonzero()
print(min_pixel_position, '\n') # tensor([[0, 2, 4, 4],
                                #         [1, 1, 3, 7],
                                #         [2, 0, 3, 1]])
```

```Python
import numpy as np
import torch
import torchvision

img = torch.randint(0, 256, (4, 3, 5, 9)).type(torch.uint8)  # (batch_size, C, H, W) = (4, 3, 5, 9)
img_scaled1 = img / img.max().float()
img_scaled2 = img_scaled3 = torch.zeros_like(img).float()

# Pixel-value scaling carried out by ToTensor is on a per-image basis in a batch
for i in range(img.shape[0]):
    """
    torchvision.transforms.ToTensor is meant to work directly on PIL representation or numpy array
    """
    # Tensor.numpy() to convert into numpy array
    # (1, 2, 0) is for reshaping from (C, H, W) to (H, W, C), which is expected by ToTensor
    img_scaled2[i] = torchvision.transforms.ToTensor()(np.transpose(img[i].numpy(), (1, 2, 0)))

print(torch.all(img_scaled1[0].eq(img_scaled2[0])))     # tensor(True)

for i in range(img.shape[0]):
    """
    torchvision.transforms.ToPILImage converts each image tensor into PIL representation
    It means reshaping (C, H, W) array into (H, W, C) array
    """
    img_scaled3[i] = torchvision.transforms.ToTensor()(torchvision.transforms.ToPILImage()(img[i]))

print(torch.all(img_scaled2[0].eq(img_scaled3[0])))     # tensor(True)

# Input Data Augmentation: Mapping [0, 1.0] range to [-1.0, +1.0]
# Must do this on a per-channel basis
img_normed1 = img_normed2 = torch.zeros_like(img).float()

# [0.5, 0.5, 0.5], [0.5, 0.5, 0.5] = subtract 0.5 and then divide by 0.5
transform_obj = torchvision.transforms.Compose([torchvision.transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
for i in range(img.shape[0]): img_normed1[i] = transform_obj(img_scaled1[i])

# Provide a list of transofmration needed
transform_obj = torchvision.transforms.Compose([
                    torchvision.transforms.ToPILImage(),
                    torchvision.transforms.ToTensor(),
                    torchvision.transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
for i in range(img.shape[0]): img_normed2[i] = transform_obj(img[i])

print(torch.all(img_normed1[0].eq(img_normed2[0])))     # tensor(True)

print(img_scaled1[0], '\n')
"""
tensor([[[0.2000, 0.4706, 0.6627, 0.7608, 0.6667, 0.7294, 0.2627, 0.3137, 0.3294],
         [0.8980, 0.5294, 0.9412, 0.4039, 0.1686, 0.6275, 0.9451, 0.7373, 0.6745],
         [0.9725, 0.1451, 0.4745, 0.5804, 0.6392, 0.6471, 0.8902, 0.3137, 0.1373],
         [0.5529, 0.3804, 0.4902, 0.1412, 0.5961, 0.6431, 0.9216, 0.9569, 0.8588],
         [0.6824, 0.9647, 0.2431, 0.2588, 0.1686, 0.2471, 0.3608, 0.1843, 0.5961]],

        [[0.0392, 0.2157, 0.2392, 0.9804, 0.3608, 0.7137, 0.3569, 0.1529, 0.6941],
         [0.2745, 0.5216, 0.1647, 0.8745, 0.3098, 0.4431, 0.7020, 0.0431, 0.7059],
         [0.7216, 0.8431, 0.9725, 0.7961, 0.5765, 0.3922, 0.0588, 0.5451, 0.3804],
         [0.7725, 0.0941, 0.3333, 0.3725, 0.0392, 0.3843, 0.8000, 0.4353, 0.1059],
         [0.3451, 0.3059, 0.6039, 0.5765, 0.6980, 0.3255, 0.8863, 0.6902, 0.3294]],

        [[0.1922, 0.3843, 0.4667, 0.5137, 0.1922, 0.1961, 0.3765, 0.8784, 0.7529],
         [0.4784, 0.9451, 0.4157, 0.9608, 0.9020, 0.1765, 0.6549, 0.3020, 0.6784],
         [1.0000, 0.3569, 0.0353, 0.7294, 0.4392, 0.0588, 0.9765, 0.6902, 0.8314],
         [0.1137, 0.1922, 0.6745, 0.7882, 1.0000, 0.0000, 0.0392, 0.3373, 0.9255],
         [0.6039, 0.0863, 0.2627, 0.6510, 0.4588, 0.9569, 0.0627, 0.3882, 0.4392]]]) 
"""

print(img_normed1[0])
# (0.2000 - 0.5) / 0.5 = -0.6
# (0.0392 - 0.5) / 0.5 = -0.9216
"""
tensor([[[-0.6000, -0.0588,  0.3255,  0.5216,  0.3333,  0.4588, -0.4745, -0.3725, -0.3412],
         [ 0.7961,  0.0588,  0.8824, -0.1922, -0.6627,  0.2549,  0.8902,  0.4745,  0.3490],
         [ 0.9451, -0.7098, -0.0510,  0.1608,  0.2784,  0.2941,  0.7804, -0.3725, -0.7255],
         [ 0.1059, -0.2392, -0.0196, -0.7176,  0.1922,  0.2863,  0.8431,  0.9137,  0.7176],
         [ 0.3647,  0.9294, -0.5137, -0.4824, -0.6627, -0.5059, -0.2784, -0.6314,  0.1922]],

        [[-0.9216, -0.5686, -0.5216,  0.9608, -0.2784,  0.4275, -0.2863, -0.6941,  0.3882],
         [-0.4510,  0.0431, -0.6706,  0.7490, -0.3804, -0.1137,  0.4039, -0.9137,  0.4118],
         [ 0.4431,  0.6863,  0.9451,  0.5922,  0.1529, -0.2157, -0.8824,  0.0902, -0.2392],
         [ 0.5451, -0.8118, -0.3333, -0.2549, -0.9216, -0.2314,  0.6000, -0.1294, -0.7882],
         [-0.3098, -0.3882,  0.2078,  0.1529,  0.3961, -0.3490,  0.7725,  0.3804, -0.3412]],

        [[-0.6157, -0.2314, -0.0667,  0.0275, -0.6157, -0.6078, -0.2471,  0.7569,  0.5059],
         [-0.0431,  0.8902, -0.1686,  0.9216,  0.8039, -0.6471,  0.3098, -0.3961,  0.3569],
         [ 1.0000, -0.2863, -0.9294,  0.4588, -0.1216, -0.8824,  0.9529,  0.3804,  0.6627],
         [-0.7725, -0.6157,  0.3490,  0.5765,  1.0000, -1.0000, -0.9216, -0.3255,  0.8510],
         [ 0.2078, -0.8275, -0.4745,  0.3020, -0.0824,  0.9137, -0.8745, -0.2235, -0.1216]]])
"""
```