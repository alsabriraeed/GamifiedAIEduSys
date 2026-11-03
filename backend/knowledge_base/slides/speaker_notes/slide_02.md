# Slide 2: Neural Networks Basics

## What to Say (30-60 seconds)

Let's start with the building block of deep learning: the artificial neuron, inspired by biological neurons in our brains. Just like biological neurons receive signals through dendrites, process them, and send outputs through axons, artificial neurons receive inputs, apply weights to them, sum them up, and pass the result through an activation function.

The simplest form is called a perceptron. It takes multiple inputs, multiplies each by a weight, adds them together with a bias term, and produces an output. Mathematically: output = activation(w₁x₁ + w₂x₂ + ... + bias).

Activation functions are crucial - they introduce non-linearity, allowing networks to learn complex patterns. The sigmoid function squashes outputs between 0 and 1, useful for probabilities. ReLU (Rectified Linear Unit) outputs the input if positive, zero otherwise - it's simple but extremely effective and is the most popular choice today.

**Check Understanding:** Why do we need activation functions? What would happen if we just used linear combinations?

## Key Points
- Artificial neurons mimic biological neurons
- Perceptron: weighted sum + bias + activation function
- Activation functions introduce non-linearity
- ReLU is the most common activation in modern networks

## Common Student Questions

**Q: Why can't we use linear functions?**
A: Without non-linear activations, stacking multiple layers would still produce a linear function. We'd lose the power to model complex, non-linear relationships.

**Q: Why is ReLU better than sigmoid?**
A: ReLU solves the "vanishing gradient" problem - sigmoid gradients get very small in deep networks, slowing learning. ReLU gradients are either 0 or 1, making training faster.

**Q: What's the bias term for?**
A: Bias allows the activation function to be shifted left or right, giving the network more flexibility in fitting data.

## Mathematical Details
```
Perceptron: y = σ(Σ(wᵢxᵢ) + b)

Sigmoid: σ(x) = 1 / (1 + e⁻ˣ)
ReLU: σ(x) = max(0, x)
Tanh: σ(x) = (eˣ - e⁻ˣ) / (eˣ + e⁻ˣ)
```
