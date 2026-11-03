# Slide 11: Regularization Techniques

## What to Say (30-60 seconds)

As networks get more powerful, they can memorize training data rather than learning generalizable patterns - this is overfitting. Regularization techniques combat this by constraining the learning process.

Dropout is brilliantly simple: during training, randomly set a fraction of neuron activations to zero with probability p (typically 0.5). This forces the network to learn redundant representations - no single neuron can be relied upon. At test time, we use all neurons but scale activations by the dropout probability. Think of it like training an ensemble of sub-networks.

L1 and L2 regularization add penalties to the loss function based on weight magnitudes. L2 penalizes the sum of squared weights, encouraging small, diffuse weights. L1 penalizes absolute values, encouraging sparsity - many weights go to exactly zero. This prevents weights from growing arbitrarily large and overfitting to noise.

Other regularization approaches include early stopping, data augmentation, batch normalization, and architectural choices like skip connections. The goal is always the same: improve generalization to unseen data.

**Check Understanding:** Why does dropout work? What's the intuition behind forcing neurons to randomly turn off?

## Key Points
- Regularization prevents overfitting to training data
- Dropout: randomly deactivate neurons during training
- L1/L2: penalize large weights in loss function
- Goal: improve generalization to test/real-world data

## Common Student Questions

**Q: When should I use dropout vs L2 regularization?**
A: Often use both! Dropout typically in fully-connected layers (0.2-0.5 rate). L2 regularization (weight decay) is standard with modern optimizers. Start with both, remove if underfitting.

**Q: Why don't we use dropout during testing?**
A: Dropout is for training only. At test time, we want the full network capacity and deterministic outputs. We scale activations by (1-p) to account for more active neurons.

**Q: What's the difference between L1 and L2?**
A: L2 (ridge): penalizes w². Encourages small weights, smooth solutions. L1 (lasso): penalizes |w|. Encourages sparsity, feature selection. L2 is standard; use L1 when you want automatic feature selection.

**Q: Can I use too much regularization?**
A: Yes! Too much causes underfitting - the network can't fit even the training data. Signs: both training and validation loss are high. Solution: reduce regularization strength, increase model capacity.

## Dropout Math
```
Training:
  mask ∼ Bernoulli(1-p)
  y = (x ⊙ mask) / (1-p)

Testing:
  y = x

Inverted dropout (PyTorch default):
  Scales during training so no scaling needed at test
```

## Regularization Terms
```
L2 (Weight Decay):
  L_total = L_data + λ Σ wᵢ²
  Common λ: 1e-4 to 1e-2

L1:
  L_total = L_data + λ Σ |wᵢ|
  
Elastic Net (combines both):
  L_total = L_data + λ₁ Σ |wᵢ| + λ₂ Σ wᵢ²
```

## Other Regularization Techniques
- **Early Stopping**: Stop training when validation loss increases
- **Data Augmentation**: Artificially expand dataset (rotate, flip, crop images)
- **Batch Normalization**: Normalizes layer inputs, has regularizing effect
- **Weight Constraints**: Clip weights to maximum norm
- **Mixup**: Train on linear combinations of examples
- **Label Smoothing**: Soften one-hot labels (0.9 instead of 1.0)
