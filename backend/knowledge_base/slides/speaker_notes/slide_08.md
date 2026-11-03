# Slide 8: Recurrent Neural Networks

## What to Say (30-60 seconds)

While CNNs excel at spatial data, Recurrent Neural Networks, or RNNs, are designed for sequential data - anything with a time or order component like text, speech, or time series.

The key idea: RNNs have loops. At each time step, the network receives input and also feeds its own output back as input for the next step. This creates a hidden state - a kind of memory that captures information from previous time steps. For example, when reading a sentence, the network builds up context word by word.

However, basic RNNs struggle with long sequences due to vanishing gradients. Enter LSTM (Long Short-Term Memory) and GRU (Gated Recurrent Unit) cells. These use gating mechanisms - learnable switches that control what information to keep, forget, or output. LSTMs have three gates: forget, input, and output. GRUs simplify this to two gates and often work just as well with less computation.

These architectures powered breakthroughs in machine translation, speech recognition, and text generation before transformers took over. They're still valuable for certain sequential tasks, especially with limited data.

**Check Understanding:** Why does a standard feedforward network fail at sequence tasks that an RNN handles well?

## Key Points
- RNNs process sequences through recurrent connections
- Hidden state acts as memory across time steps
- Vanilla RNNs suffer from vanishing gradients in long sequences
- LSTM/GRU use gates to maintain long-term dependencies

## Common Student Questions

**Q: LSTM vs GRU - which is better?**
A: GRU is simpler (fewer parameters, faster training). LSTM has more capacity for complex patterns. In practice, try both - GRU often works just as well. Start with GRU, switch to LSTM if needed.

**Q: How do I handle variable-length sequences?**
A: Padding (add zeros to make all sequences same length) or packing (PyTorch's pack_padded_sequence). Always mask padded positions during loss calculation.

**Q: Can RNNs work bidirectionally?**
A: Yes! Bidirectional RNNs process sequences forward and backward, capturing both past and future context. Excellent for tasks where you have the full sequence (like text classification), not online prediction.

**Q: Why did transformers replace RNNs?**
A: RNNs process sequentially (slow, can't parallelize). Transformers process entire sequence at once via attention (faster, better long-range dependencies). But RNNs still useful for streaming data or embedded systems.

## LSTM Cell Internals
```
Forget gate: fₜ = σ(Wf·[hₜ₋₁, xₜ] + bf)
Input gate:  iₜ = σ(Wi·[hₜ₋₁, xₜ] + bi)
Cell update: c̃ₜ = tanh(Wc·[hₜ₋₁, xₜ] + bc)
Cell state:  cₜ = fₜ ⊙ cₜ₋₁ + iₜ ⊙ c̃ₜ
Output gate: oₜ = σ(Wo·[hₜ₋₁, xₜ] + bo)
Hidden:      hₜ = oₜ ⊙ tanh(cₜ)

Where ⊙ is element-wise multiplication
```

## Applications
- Text generation (character/word level)
- Machine translation (encoder-decoder)
- Speech recognition
- Time series forecasting
- Video analysis (frame sequences)
- Music generation
