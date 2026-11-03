# Slide 4: Loss Functions

## What to Say (30-60 seconds)

A loss function is how we measure how wrong our network's predictions are. It's the compass that guides learning - the network adjusts its weights to minimize this loss.

For regression problems - predicting continuous values like house prices - we typically use Mean Squared Error, or MSE. It calculates the squared difference between predicted and actual values, then averages across all examples. Why squared? It penalizes larger errors more heavily and makes the math work nicely for gradient descent.

For classification - predicting categories - we use Cross-Entropy Loss. It measures how different our predicted probability distribution is from the true distribution. If we predict 80% confidence for the correct class, the loss is lower than if we predicted 20%. Cross-entropy is perfect for use with softmax outputs.

The choice of loss function deeply affects what your network learns to optimize. Choose MSE when you care about exact numerical accuracy. Choose cross-entropy when you care about confident, correct classifications.

**Check Understanding:** Why do you think we square the errors in MSE rather than just taking absolute differences?

## Key Points
- Loss function measures prediction error
- MSE for regression: average of squared differences
- Cross-entropy for classification: measures probability distribution difference
- Loss guides the optimization process

## Common Student Questions

**Q: Can I use MSE for classification?**
A: Technically yes, but cross-entropy works much better. MSE with softmax can cause "saturation" - when very wrong predictions produce tiny gradients, slowing learning.

**Q: What's the difference between loss and accuracy?**
A: Loss is continuous and differentiable - needed for gradient descent. Accuracy is discrete (% correct) - easy to interpret but can't be directly optimized with gradients.

**Q: Are there other loss functions?**
A: Many! Huber loss (robust to outliers), Focal loss (for imbalanced classes), Contrastive loss (for similarity learning), and more. Each designed for specific problem types.

## Mathematical Formulas
```
MSE: L = (1/n) Σ(yᵢ - ŷᵢ)²

Cross-Entropy (binary): L = -[y log(ŷ) + (1-y) log(1-ŷ)]

Cross-Entropy (multi-class): L = -Σ yᵢ log(ŷᵢ)
where y is one-hot encoded true label
```
