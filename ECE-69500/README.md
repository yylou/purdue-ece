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

'''
np.array[150, 100, :]       = (H, W, C)
img.getpixel((100, 150))    = (W, H)
torch.array[:, 150, 100]    = (C, H, W)
'''
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

