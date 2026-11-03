# Slide 6: Gradient Descent

## What to Say (30-60 seconds)

Gradient descent is the optimization algorithm that uses those gradients from backpropagation to actually update the weights. Think of it as the strategy for navigating down that mountain we mentioned.

The basic algorithm is simple: calculate gradients, multiply by a learning rate (step size), and subtract from current weights. The learning rate is critical - too large and you overshoot the minimum, bouncing around wildly. Too small and training takes forever.

In practice, we use variants that work much better than basic gradient descent. Stochastic Gradient Descent, or SGD, updates weights after each mini-batch of examples rather than the full dataset - much faster and adds beneficial noise. Adam, the most popular optimizer today, adapts the learning rate for each weight based on movement history, combining momentum and adaptive learning rates.

Modern best practice: start with Adam optimizer with default learning rate 0.001. It's robust and works well across many problems without much tuning.

**Check Understanding:** Why might a constant learning rate be problematic throughout training? Should we maybe decrease it over time?

## Key Points
- Gradient descent: iteratively update weights to minimize loss
- Learning rate controls step size - critical hyperparameter  
- SGD: updates per mini-batch, faster and adds regularization
- Adam: adaptive learning rates per parameter, most popular today

## Common Student Questions

**Q: How do I choose learning rate?**
A: Start with 0.001 (Adam default). If training is unstable, reduce by 10×. If too slow, increase. Many practitioners use learning rate schedules that decrease over time.

**Q: What's the difference between SGD, momentum, and Adam?**
A: SGD updates in gradient direction. Momentum adds fraction of previous update (like a ball rolling downhill). Adam combines momentum with adaptive per-parameter learning rates - generally best.

**Q: What's a mini-batch?**
A: A subset of training data (typically 32-256 examples) used to compute one gradient update. Balances speed (larger batches utilize GPUs better) with generalization (smaller batches add noise).

**Q: Can we use different learning rates for different layers?**
A: Yes! Advanced technique: freeze early layers (learning rate = 0), fine-tune later layers. Or use discriminative learning rates: smaller for early layers, larger for later ones.

## Algorithms Comparison
```
Basic GD:
  w ← w - α∇L(w)

SGD with Momentum:
  vₜ ← βvₜ₋₁ + ∇L(w)
  w ← w - αvₜ

Adam:
  mₜ ← β₁mₜ₋₁ + (1-β₁)∇L(w)    # first moment
  vₜ ← β₂vₜ₋₁ + (1-β₂)(∇L(w))² # second moment
  w ← w - α·mₜ/√(vₜ + ε)
```

## Typical Hyperparameters
- Adam: α=0.001, β₁=0.9, β₂=0.999, ε=1e-8
- SGD + Momentum: α=0.01-0.1, β=0.9
- Batch size: 32, 64, 128, or 256
