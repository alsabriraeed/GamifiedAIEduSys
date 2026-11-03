# Slide 12: Best Practices & Next Steps

## What to Say (30-60 seconds)

Let's close with practical advice to set you up for success in your deep learning journey.

Data preprocessing is critical - your model is only as good as your data. Normalize inputs to zero mean and unit variance. Handle missing values. For images, subtract mean pixel values. Split data properly: training, validation (for hyperparameters), and test (for final evaluation). Never let your model see test data during development!

Hyperparameter tuning is part science, part art. Start with proven defaults: Adam optimizer with learning rate 0.001, batch size 32-128, initializations like He or Xavier. Then tune systematically - don't change everything at once. Modern approaches like Bayesian optimization or random search beat manual tuning.

For continuous learning: stay current with papers on arXiv, especially categories like cs.LG and cs.CV. Implement papers from scratch - nothing builds understanding like coding. Contribute to open source projects. Enter Kaggle competitions. And most importantly: work on projects you care about - passion drives learning.

The field evolves rapidly, but fundamentals remain. Master the basics we've covered, and you'll adapt to whatever comes next.

**Final Question:** What topic from this course will you explore first in your own projects?

## Key Points
- Proper data preprocessing is foundational
- Start with proven hyperparameter defaults, tune systematically
- Continuous learning through papers, projects, competitions
- Deep learning evolves fast - strong fundamentals enable adaptation

## Common Student Questions

**Q: How do I choose the right architecture for my problem?**
A: Start with proven architectures: CNNs for images, Transformers for text/sequences, simple feedforward for tabular data. Use transfer learning when possible (pretrained models). Iterate from simple to complex.

**Q: How much data do I need?**
A: Depends on complexity. Simple tasks: thousands of examples. Complex tasks (ImageNet-scale): millions. Transfer learning dramatically reduces data requirements - fine-tuning pretrained models works with hundreds of examples.

**Q: My model isn't learning - what do I check?**
A: Debug checklist:
  1. Can you overfit a tiny batch? (if no: bug in model/loss)
  2. Is loss decreasing? (if no: learning rate too high/low)
  3. Check gradients (vanishing/exploding?)
  4. Verify data pipeline (labels correct?)
  5. Simplify architecture

**Q: GPU vs CPU - how important is hardware?**
A: For learning: CPU is fine for small models/datasets. For real work: GPU is essential - 10-100× faster. Google Colab offers free GPUs. Cloud options: AWS, GCP, Lambda Labs.

## Data Preprocessing Checklist
```python
# Normalization
X = (X - X.mean()) / X.std()

# Train/Val/Test split
# 70/15/15 or 80/10/10

# Image specific
X = X / 255.0  # Scale to [0,1]
# or subtract ImageNet means

# Handle class imbalance
# - Weighted loss
# - Oversampling minority class
# - Data augmentation
```

## Hyperparameter Starting Points
```
Optimizer: Adam
Learning rate: 1e-3 (try 1e-2, 1e-4 if needed)
Batch size: 32-128 (larger if GPU memory allows)
Epochs: 50-100 (with early stopping)
Weight decay (L2): 1e-4
Dropout: 0.2-0.5 in fully connected layers
Initialization: He (for ReLU), Xavier (for tanh/sigmoid)
```

## Learning Resources
- **Papers**: arXiv.org (cs.LG, cs.CV, cs.CL)
- **Courses**: 
  - Stanford CS231n (CNNs)
  - Fast.ai (practical deep learning)
  - Coursera Deep Learning Specialization
- **Books**:
  - "Deep Learning" (Goodfellow, Bengio, Courville)
  - "Dive into Deep Learning" (d2l.ai - interactive)
- **Practice**:
  - Kaggle competitions
  - Papers with Code (implementations)
  - PyTorch/TensorFlow tutorials
- **Communities**:
  - Reddit: r/MachineLearning
  - Twitter: #ML, #DeepLearning
  - Discord: ML/AI servers

## Parting Wisdom
"The best way to learn deep learning is to do deep learning. Pick a problem you care about, find a dataset, and start building. You'll learn more from one completed project than from ten unfinished tutorials."
