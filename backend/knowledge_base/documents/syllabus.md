# Deep Learning Fundamentals - Course Syllabus

## Course Overview

This course provides a comprehensive introduction to deep learning, covering fundamental concepts, architectures, and practical applications. Students will gain both theoretical understanding and hands-on experience with modern deep learning frameworks.

## Learning Objectives

By the end of this course, students will be able to:

1. **Understand Neural Network Fundamentals**
   - Explain how artificial neurons work and their biological inspiration
   - Implement forward propagation in multi-layer networks
   - Describe the role of activation functions and choose appropriate ones

2. **Master Training Algorithms**
   - Derive and implement backpropagation using the chain rule
   - Configure gradient descent optimizers (SGD, Adam, RMSprop)
   - Calculate and minimize various loss functions

3. **Apply Specialized Architectures**
   - Design and train Convolutional Neural Networks for computer vision
   - Implement Recurrent Neural Networks for sequential data
   - Understand attention mechanisms and transformer architecture

4. **Prevent Overfitting**
   - Apply regularization techniques (dropout, L1/L2)
   - Use data augmentation and early stopping
   - Diagnose and fix underfitting/overfitting

5. **Deploy Models Effectively**
   - Preprocess data appropriately for different domains
   - Tune hyperparameters systematically
   - Evaluate models using proper train/validation/test splits

## Course Topics

### Module 1: Foundations (Slides 1-3)
- Introduction to deep learning
- Neural network basics: perceptrons and activation functions  
- Building multi-layer networks
- Forward propagation

### Module 2: Training Fundamentals (Slides 4-6)
- Loss functions: MSE and cross-entropy
- Backpropagation and the chain rule
- Gradient descent and optimization algorithms
- Learning rates and convergence

### Module 3: Convolutional Networks (Slide 7)
- Motivation: Why CNNs for images?
- Convolution operation and filters
- Pooling layers and dimensionality reduction
- Famous architectures: LeNet, AlexNet, ResNet, VGG

### Module 4: Sequential Models (Slide 8)
- Recurrent Neural Networks (RNNs)
- Vanishing/exploding gradients problem
- LSTM and GRU architectures
- Applications: text, speech, time series

### Module 5: Modern Architectures (Slides 9-10)
- Attention mechanisms
- Query-Key-Value framework
- Transformer architecture
- Multi-head attention
- Modern applications: BERT, GPT, Vision Transformers

### Module 6: Practical Deep Learning (Slides 11-12)
- Regularization techniques
- Best practices for data preprocessing
- Hyperparameter tuning strategies
- Resources for continued learning

## Prerequisites

- **Mathematics**: Calculus (derivatives, chain rule), Linear Algebra (matrices, vectors, dot products)
- **Programming**: Python basics (variables, functions, loops, classes)
- **Machine Learning**: Basic familiarity with supervised learning concepts helpful but not required

## Required Software

- Python 3.8+
- PyTorch or TensorFlow
- NumPy, Matplotlib
- Jupyter Notebook
- (Optional) CUDA for GPU acceleration

## Assessment

- **Problem Sets** (40%): Weekly coding assignments implementing concepts from scratch
- **Midterm Project** (25%): Train a CNN for kaggle image classification competition
- **Final Project** (35%): Open-ended project applying deep learning to your domain of interest

## Textbooks and Resources

### Primary Textbook
- Goodfellow, Bengio, and Courville. "Deep Learning" (MIT Press, 2016)
  - Free online: https://www.deeplearningbook.org/

### Supplementary Resources
- "Dive into Deep Learning" - Interactive online textbook (d2l.ai)
- PyTorch Tutorials: pytorch.org/tutorials
- Stanford CS231n lecture notes
- Papers: "Attention is All You Need", "Deep Residual Learning", "BERT", "GPT-3"

## Course Schedule (12 Weeks)

**Week 1**: Introduction & Neural Network Basics  
**Weeks 2-3**: Training (Loss, Backprop, Optimization)  
**Weeks 4-5**: Convolutional Neural Networks  
**Week 6**: Midterm Project  
**Weeks 7-8**: Recurrent Neural Networks  
**Weeks 9-10**: Attention & Transformers  
**Week 11**: Regularization & Best Practices  
**Week 12**: Final Project Presentations

## Office Hours

- Instructor Office Hours: Wednesdays 2-4pm
- TA Office Hours: Mondays 3-5pm, Fridays 1-3pm
- Online Q&A: Course Discord server (get help anytime)

## Academic Integrity

All code submissions must be your own work. You may discuss concepts with peers but must implement solutions independently. Properly cite any external code or resources used. Use of ChatGPT or similar tools is allowed for debugging and learning but final submissions must demonstrate your understanding.

## Tips for Success

1. **Code along with lectures** - Don't just watch, implement
2. **Start assignments early** - Deep learning experiments take time to run
3. **Use office hours** - Get help when stuck, don't struggle alone
4. **Read papers** - Exposure to research builds intuition
5. **Work on projects you care about** - Passion drives learning
