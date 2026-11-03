# Slide 7: Convolutional Neural Networks

## What to Say (30-60 seconds)

Convolutional Neural Networks, or CNNs, are specifically designed for image data and have revolutionized computer vision. Why do we need a special architecture? Regular neural networks treat images as flat vectors, losing spatial relationship information and requiring enormous numbers of parameters.

CNNs solve this with the convolution operation. A small filter, or kernel - say 3×3 pixels - slides across the image, computing dot products at each position. This produces a feature map highlighting where certain patterns appear. Early layers detect simple features like edges. Deeper layers combine these into complex patterns like textures, parts, then whole objects.

Pooling layers downsample feature maps, reducing dimensions while keeping important information. Max pooling takes the maximum value in each region - retaining the strongest signal while making the network robust to small shifts in position.

The genius of CNNs: parameter sharing (same filter across entire image) and local connectivity (each neuron only sees a small region) dramatically reduce parameters while capturing spatial structure.

**Check Understanding:** Why does a CNN need far fewer parameters than a fully connected network for the same image? Think about parameter sharing!

## Key Points
- CNNs designed for spatial data (images, video)
- Convolution: sliding filters extract local features
- Hierarchical learning: edges → textures → parts → objects
- Pooling reduces dimensions, adds translation invariance

## Common Student Questions

**Q: What size filters should I use?**
A: 3×3 is most common (proven effective in ResNet, VGG). Occasionally 5×5 or 7×7 for first layer. Stack multiple 3×3 layers instead of one large filter.

**Q: How many filters per layer?**
A: Typical progression: 32 → 64 → 128 → 256 as layers deepen. Each filter learns a different pattern.

**Q: Average pooling vs max pooling?**
A: Max pooling is most common - retains strongest activations. Average pooling sometimes used before final classification layer. Stride-2 convolutions increasingly replace pooling entirely.

**Q: Why are CNNs translation invariant?**
A: Parameter sharing means the same filter detects the same pattern anywhere in the image. Pooling further reduces sensitivity to exact position.

## Architecture Example
```
Input: 224×224×3 RGB image

Conv1: 64 filters, 3×3, ReLU → 224×224×64
Pool1: 2×2 max pool, stride 2 → 112×112×64

Conv2: 128 filters, 3×3, ReLU → 112×112×128
Pool2: 2×2 max pool, stride 2 → 56×56×128

Conv3: 256 filters, 3×3, ReLU → 56×56×256
Pool3: 2×2 max pool, stride 2 → 28×28×256

Flatten → Fully Connected → Output
```

## Famous CNN Architectures
- LeNet-5 (1998): First successful CNN, digits
- AlexNet (2012): ImageNet breakthrough
- VGG (2014): Very deep with small filters
- ResNet (2015): Residual connections, 100+ layers
- EfficientNet (2019): Optimized accuracy/efficiency
