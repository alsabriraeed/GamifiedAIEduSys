# Slide 3: Building Multi-Layer Networks

## What to Say (30-60 seconds)

Now let's connect these neurons into a network. A multi-layer neural network consists of three types of layers: the input layer, which receives your data; one or more hidden layers, where the magic happens; and the output layer, which produces predictions.

Forward propagation is how we compute predictions. Data flows from input to output: each layer receives inputs from the previous layer, applies weights and activations, and passes results to the next layer. For example, if you're classifying images, the input layer might receive pixel values, hidden layers extract features like edges then shapes, and the output layer predicts the class.

The architecture - how many layers and how many neurons per layer - is crucial. More layers can learn more complex patterns, but also require more data and computation. A typical starting point might be 2-3 hidden layers with 64-256 neurons each, but this varies widely by problem.

**Check Understanding:** If each layer just passes information forward, how does the network actually "learn"? We'll answer that soon with backpropagation!

## Key Points
- Three layer types: input, hidden, output
- Forward propagation: data flows input → output
- Each layer transforms its input through weights + activations
- Architecture depth and width affect learning capacity

## Common Student Questions

**Q: How many hidden layers should I use?**
A: Start with 2-3 layers. Add more if the model underfits (poor training accuracy). Modern networks can have hundreds of layers for complex tasks like image recognition.

**Q: How many neurons per layer?**
A: Common practice: start with 64-256 neurons, adjust based on problem complexity. More neurons = more capacity but higher risk of overfitting.

**Q: Can layers have different numbers of neurons?**
A: Absolutely! Common pattern: start wide, gradually narrow toward output. Example: 256 → 128 → 64 → 10 (for 10-class classification).

## Example Architecture
```
Input: 784 neurons (28×28 MNIST image flattened)
Hidden 1: 256 neurons, ReLU activation
Hidden 2: 128 neurons, ReLU activation  
Output: 10 neurons, Softmax activation (for 10 digit classes)
```
