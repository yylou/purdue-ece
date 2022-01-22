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