# Deep Learning Fundamentals - Detailed Reference

This document provides in-depth explanations, mathematical derivations, and code examples for concepts covered in the Deep Learning Fundamentals course.

## 1. Neural Networks and Perceptrons

### Mathematical Foundation

A perceptron is a linear classifier that computes:

```
ŷ = σ(w·x + b)
```

Where:
- `x` = input vector [x₁, x₂, ..., xₙ]
- `w` = weight vector [w₁, w₂, ..., wₙ]
- `b` = bias (scalar)
- `σ` = activation function
- `ŷ` = output prediction

### Common Activation Functions

**Sigmoid**: Maps input to (0, 1)
```
σ(z) = 1 / (1 + e⁻ᶻ)
Derivative: σ'(z) = σ(z)(1 - σ(z))
```
Use case: Binary classification output, gate functions in LSTMs

**Tanh**: Maps input to (-1, 1)
```
tanh(z) = (eᶻ - e⁻ᶻ) / (eᶻ + e⁻ᶻ)
Derivative: tanh'(z) = 1 - tanh²(z)
```
Use case: RNN hidden states (zero-centered output)

**ReLU** (Rectified Linear Unit): Most popular in deep networks
```
ReLU(z) = max(0, z)
Derivative: 1 if z > 0, else 0
```
Use case: Default choice for hidden layers in feedforward and CNNs

**Leaky ReLU**: Addresses "dying ReLU" problem
```
LeakyReLU(z) = max(αz, z) where α = 0.01
```

**Softmax**: For multi-class classification
```
softmax(z)ᵢ = eᶻⁱ / Σⱼ eᶻʲ
```
Outputs probability distribution over classes

### PyTorch Implementation

```python
import torch
import torch.nn as nn

class SimplePerceptron(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, output_dim)
    
    def forward(self, x):
        return torch.sigmoid(self.linear(x))

# Multi-layer network
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
    
    def forward(self, x):
        return self.layers(x)
```

## 2. Forward Propagation

Forward propagation computes the output of a network layer by layer.

For a single layer:
```
z[l] = W[l] @ a[l-1] + b[l]
a[l] = σ(z[l])
```

Where:
- `a[l]` = activation of layer l
- `W[l]` = weight matrix for layer l
- `b[l]` = bias vector for layer l
- `σ` = activation function
- `@` = matrix multiplication

### Example: 3-Layer Network

```
Input: x ∈ ℝ⁴
Layer 1: 4 → 8 neurons, ReLU
Layer 2: 8 → 6 neurons, ReLU  
Output: 6 → 3 neurons, Softmax

z¹ = W¹x + b¹        # (8×4) @ (4×1) + (8×1) = (8×1)
a¹ = ReLU(z¹)        # (8×1)
z² = W²a¹ + b²       # (6×8) @ (8×1) + (6×1) = (6×1)
a² = ReLU(z²)        # (6×1)
z³ = W³a² + b³       # (3×6) @ (6×1) + (3×1) = (3×1)
ŷ = softmax(z³)      # (3×1) - probability distribution
```

## 3. Loss Functions

### Mean Squared Error (MSE)

**Formula:**
```
L = (1/n) Σᵢ (yᵢ - ŷᵢ)²
```

**Gradient:**
```
∂L/∂ŷ = (2/n)(ŷ - y)
```

**Use case:** Regression tasks where output is continuous

**PyTorch:**
```python
criterion = nn.MSELoss()
loss = criterion(predictions, targets)
```

### Cross-Entropy Loss

**Binary Cross-Entropy:**
```
L = -(1/n) Σᵢ [yᵢ log(ŷᵢ) + (1-yᵢ) log(1-ŷᵢ)]
```

**Categorical Cross-Entropy:**
```
L = -(1/n) Σᵢ Σⱼ yᵢⱼ log(ŷᵢⱼ)
```
Where y is one-hot encoded

**Gradient (with softmax):**
```
∂L/∂zⱼ = ŷⱼ - yⱼ  (remarkably simple!)
```

**PyTorch:**
```python
# Binary
criterion = nn.BCEWithLogitsLoss()  #includes sigmoid

# Multi-class  
criterion = nn.CrossEntropyLoss()  # includes softmax
loss = criterion(logits, target_classes)
```

## 4. Backpropagation Derivation

### Single Layer

Given:
```
L = loss(ŷ, y)
ŷ = σ(z)
z = wx + b
```

Compute gradients:
```
∂L/∂b = ∂L/∂z = ∂L/∂ŷ · ∂ŷ/∂z = ∂L/∂ŷ · σ'(z)

∂L/∂w = ∂L/∂z more · ∂z/∂w = (∂L/∂ŷ · σ'(z)) · x

∂L/∂x = ∂L/∂z · ∂z/∂x = (∂L/∂ŷ · σ'(z)) · w
```

### Multi-Layer Network

For layer l:
```
∂L/∂W[l] = ∂L/∂a[l] · ∂a[l]/∂z[l] · ∂z[l]/∂W[l]
         = δ[l] @ a[l-1]ᵀ

∂L/∂b[l] = δ[l]

where δ[l] = ∂L/∂z[l] (local gradient)

δ[l] = (W[l+1]ᵀ @ δ[l+1]) ⊙ σ'(z[l])
```

The chain continues backward through the network.

### NumPy Implementation (Educational)

```python
import numpy as np

class TwoLayerNet:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
    
    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = np.maximum(0, self.z1)  # Batch normalization
        self.z2 = self.a1 @ self.W2 + self.b2
        exp_scores = np.exp(self.z2)
        self.probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        return self.probs
    
    def backward(self, X, y, learning_rate):
        m = X.shape[0]
        
        # Output layer gradient
        delta3 = self.probs.copy()
        delta3[range(m), y] -= 1
        
        # Hidden layer gradients
        dW2 = (self.a1.T @ delta3) / m
        db2 = np.sum(delta3, axis=0, keepdims=True) / m
        
        delta2 = (delta3 @ self.W2.T) * (self.z1 > 0)  # ReLU derivative
        dW1 = (X.T @ delta2) / m
        db1 = np.sum(delta2, axis=0, keepdims=True) / m
        
        # Update weights
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
```

## 5. Optimization Algorithms

### Gradient Descent Variants

**Batch Gradient Descent:** Use full dataset
- Pros: Stable, deterministic
- Cons: Slow for large datasets

**Stochastic Gradient Descent (SGD):** One example at a time
- Pros: Fast, can escape local minima
- Cons: Noisy updates, needs learning rate decay

**Mini-batch Gradient Descent:** Best of both (batch size 32-256)
- Pros: Efficient GPU utilization, somewhat stable
- Cons: Needs hyperparameter tuning

### Momentum

Accelerates SGD by accumulating velocity:
```
vₜ = βvₜ₋₁ + ∇L(θₜ)
θₜ₊₁ = θₜ - αvₜ
```
Typical β = 0.9

### Adam (Adaptive Moment Estimation)

Combines momentum with adaptive learning rates:
```
mₜ = β₁mₜ₋₁ + (1-β₁)∇L(θ)      # First moment (mean)
vₜ = β₂vₜ₋₁ + (1-β₂)(∇L(θ))²   # Second moment (variance)

m̂ₜ = mₜ/(1-β₁ᵗ)                # Bias correction
v̂ₜ = vₜ/(1-β₂ᵗ)

θₜ₊₁ = θₜ - α · m̂ₜ/(√v̂ₜ + ε)
```

Defaults: α=0.001, β₁=0.9, β₂=0.999, ε=1e-8

**PyTorch:**
```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    loss.backward()
    optimizer.step()
```

## 6. Convolutional Neural Networks

### Convolution Operation

For input I and kernel K:
```
(I * K)(i,j) = ΣₘΣₙ I(i+m, j+n) · K(m,n)
```

**Parameters:**
- Kernel size: typically 3×3 or 5×5
- Stride: step size (usually 1 or 2)
- Padding: border pixels added (0 for valid, maintain size for same)

**Output dimensions:**
```
output_height = (input_height - kernel_height + 2×padding) / stride + 1
output_width = (input_width - kernel_width + 2×padding) / stride + 1
```

### CNN Layer Types

**Conv2D:**
```python
nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, stride=1, padding=1)
# Input: (batch, 3, H, W)
# Output: (batch, 64, H, W)  # same size due to padding=1
```

**MaxPool2D:**
```python
nn.MaxPool2d(kernel_size=2, stride=2)
# Reduces spatial dimensions by half
```

**BatchNorm2D:**
```python
nn.BatchNorm2d(num_features=64)
# Normalizes activations, speeds training
```

### Example CNN

```python
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 224 → 112
            
            # Block 2
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 112 → 56
            
            # Block 3
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 56 → 28
        )
        
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),  # Global average pooling
            nn.Flatten(),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
```

## 7. Recurrent Neural Networks

### Basic RNN Cell

```
hₜ = tanh(Wₕhₜ₋₁ + Wₓxₜ + b)
yₜ = Wᵧhₜ + c
```

Where hₜ is hidden state carrying information forward in time.

### LSTM Cell

**Gates:**
```
fₜ = σ(Wf · [hₜ₋₁, xₜ] + bf)  # Forget gate
iₜ = σ(Wi · [hₜ₋₁, xₜ] + bi)  # Input gate
oₜ = σ(Wo · [hₜ₋₁, xₜ] + bo)  # Output gate
```

**Cell update:**
```
c̃ₜ = tanh(Wc · [hₜ₋₁, xₜ] + bc)  # Candidate values
cₜ = fₜ ⊙ cₜ₋₁ + iₜ ⊙ c̃ₜ          # New cell state
hₜ = oₜ ⊙ tanh(cₜ)                  # New hidden state
```

**PyTorch:**
```python
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                           batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        # x: (batch, seq_len, input_size)
        out, (hn, cn) = self.lstm(x)
        # out: (batch, seq_len, hidden_size)
        out = self.fc(out[:, -1, :])  # Last time step
        return out
```

## 8. Attention and Transformers

### Scaled Dot-Product Attention

```
Attention(Q, K, V) = softmax(QKᵀ/√dₖ) V
```

Where:
- Q = queries (what we're looking for)
- K = keys (what we have)
- V = values (actual information)
- dₖ = dimension of keys (for scaling)

### Multi-Head Attention

```
MultiHead(Q,K,V) = Concat(head₁,...,headₕ)Wₒ

where headᵢ = Attention(QWᵢq, KWᵢk, VWᵢv)
```

**PyTorch:**
```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # Linear projections and reshape for multi-head
        Q = self.W_q(Q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1,2)
        K = self.W_k(K).view(batch_size, -1, self.num_heads, self.d_k).transpose(1,2)
        V = self.W_v(V).view(batch_size, -1, self.num_heads, self.d_k).transpose(1,2)
        
        # Scaled dot-product attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attention = torch.softmax(scores, dim=-1)
        
        # Apply attention to values
        context = torch.matmul(attention, V)
        
        # Concatenate heads and project
        context = context.transpose(1,2).contiguous().view(batch_size, -1, self.d_model)
        output = self.W_o(context)
        
        return output, attention
```

## 9. Regularization Techniques

### Dropout

Randomly zero out activations during training:
```python
class DropoutExample(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(100, 50)
        self.dropout = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(50, 10)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)  # Only active during training
        x = self.fc2(x)
        return x

# Automatically handled:
model.train()  # Dropout active
model.eval()   # Dropout inactive
```

### Weight Decay (L2 Regularization)

```python
# Add to optimizer
optimizer = torch.optim.Adam(model.parameters(), 
                            lr=1e-3, 
                            weight_decay=1e-4)  # L2 penalty
```

### Early Stopping

```python
best_val_loss = float('inf')
patience = 10
counter = 0

for epoch in range(num_epochs):
    train_loss = train_one_epoch()
    val_loss = validate()
    
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(model.state_dict(), 'best_model.pth')
        counter = 0
    else:
        counter += 1
        if counter >= patience:
            print("Early stopping")
            break
```

## 10. Practical Tips and Common Pitfalls

### Weight Initialization

**He Initialization** (for ReLU):
```python
nn.init.kaiming_normal_(layer.weight, mode='fan_in', nonlinearity='relu')
```

**Xavier Initialization** (for tanh/sigmoid):
```python
nn.init.xavier_normal_(layer.weight)
```

### Learning Rate Schedules

```python
scheduler = torch.optim.lr_scheduler.StepLR(optimizer,step_size=30, gamma=0.1)
# or
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

for epoch in range(num_epochs):
    train()
    scheduler.step()
```

### Batch Normalization

Normalize layer inputs to stabilize training:
```python
nn.BatchNorm1d(num_features)  # For fully connected
nn.BatchNorm2d(num_features)  # For convolutional
```

### Gradient Clipping

Prevent exploding gradients:
```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

### Common Debugging Steps

1. **Overfit a single batch** - If model can't, there's a bug
2. **Check data pipeline** - Visualize batches, verify labels
3. **Monitor gradients** - Log norms, watch for vanishing/exploding
4. **Start simple** - Small model, small dataset, verify it works
5. **Compare to baselines** - Random guessing, simple model benchmarks
