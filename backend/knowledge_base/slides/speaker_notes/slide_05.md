# Slide 5: Backpropagation

## What to Say (30-60 seconds)

Now for the heart of deep learning: backpropagation. This is how neural networks actually learn. It's an elegant application of the chain rule from calculus to efficiently compute gradients.

Here's the idea: after forward propagation gives us predictions and we calculate the loss, we need to know how to adjust each weight to reduce that loss. Backpropagation computes the gradient - the rate of change of loss with respect to each weight - by working backwards through the network.

Starting from the output, we calculate how the loss changes with respect to the output layer's weights. Then, using the chain rule, we propagate these gradients backward through each layer. Each layer receives gradients from the layer above, computes its own gradients, and passes them to the layer below.

The beauty is efficiency: instead of computing gradients for millions of weights independently (impossibly slow), backpropagation reuses computations, making it tractable to train massive networks.

**Check Understanding:** Why do we need calculus and the chain rule? Can you see why going backward saves computation compared to checking each weight individually?

## Key Points
- Backpropagation computes gradients efficiently using chain rule
- Works backward from output loss to input weights
- Each layer computes: ∂L/∂w using gradients from next layer
- Makes training deep networks computationally feasible

## Common Student Questions

**Q: Do I need to implement backpropagation myself?**
A: Frameworks like PyTorch and TensorFlow do this automatically via "automatic differentiation" (autograd). But understanding it helps debug and design better networks.

**Q: What's the vanishing gradient problem?**
A: In very deep networks with certain activations (like sigmoid), gradients can become extremely small as they backpropagate, making early layers learn very slowly. ReLU helps mitigate this.

**Q: What's the exploding gradient problem?**
A: The opposite - gradients become very large, causing unstable training. Solutions: gradient clipping, careful initialization, batch normalization.

## The Math (Simplified)
```
Forward: z = wx + b, a = σ(z)
Loss: L(ŷ, y)

Backward (chain rule):
∂L/∂w = ∂L/∂a × ∂a/∂z × ∂z/∂w
∂L/∂w = ∂L/∂a × σ'(z) × x

Update: w ← w - α(∂L/∂w)
where α is learning rate
```

## Intuition
Think of it like hiking down a mountain in fog. You can't see the bottom, but you can feel which direction is steepest downward (the gradient). Take a step in that direction, recalculate, and repeat. Eventually you reach the valley (minimum loss).
