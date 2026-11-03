# Slide 10: Transformers

## What to Say (30-60 seconds)

The Transformer architecture, introduced in the "Attention is All You Need" paper, revolutionized deep learning by ditching recurrence entirely in favor of pure attention mechanisms.

The architecture has an encoder-decoder structure. The encoder processes the input sequence through multiple layers of multi-head self-attention and feedforward networks. Multi-head attention runs several attention operations in parallel with different learned projections, allowing the model to attend to different aspects - maybe one head captures syntax, another semantics.

The decoder generates output autoregressively, using both self-attention on generated tokens and cross-attention to the encoder output. Positional encodings are added since, unlike RNNs, transformers have no inherent sequence order.

Why did transformers win? They parallelize completely - processing all positions simultaneously rather than sequentially. They scale incredibly well with data and compute. And they've proven effective far beyond NLP: vision transformers for images, audio transformers for speech, and multi-modal transformers combining different data types.

**Check Understanding:** Why can transformers process sequences in parallel while RNNs cannot?

## Key Points
- Architecture: stacked attention + feedforward layers
- Multi-head attention: multiple parallel attention mechanisms
- Parallelizable: processes entire sequence at once
- Foundation for GPT, BERT, Vision Transformers, and more

## Common Student Questions

**Q: What does "multi-head" mean exactly?**
A: Instead of one attention operation, run h parallel attention operations (typically h=8 or 16) with different learned weight matrices. Concatenate results and project. Allows attending to different representation subspaces.

**Q: What are positional encodings?**
A: Since attention is position-agnostic, we add position information via sinusoidal functions or learned embeddings. This tells the model "this is word 1, this is word 2, etc."

**Q: Encoder-only vs decoder-only vs encoder-decoder?**
A: BERT (encoder-only) for understanding tasks (classification, QA). GPT (decoder-only) for generation. T5/BART (encoder-decoder) for seq2seq like translation. Each suited to different use cases.

**Q: Why are transformers so big (billions of parameters)?**
A: They scale well - performance improves with size. Plus: vocabulary embeddings, multiple attention heads, many layers (96+ in GPT-3), large feedforward dimensions. But efficiency research is making smaller models competitive.

## Architecture Components
```
Input → Embeddings + Positional Encoding

Encoder (Nx layers):
  - Multi-Head Self-Attention
  - Add & Normalize  
  - Feedforward Network
  - Add & Normalize

Decoder (Nx layers):
  - Masked Multi-Head Self-Attention
  - Add & Normalize
  - Multi-Head Cross-Attention (to encoder)
  - Add & Normalize
  - Feedforward Network
  - Add & Normalize

Output Projection → Softmax
```

## Multi-Head Attention
```
MultiHead(Q,K,V) = Concat(head₁,...,headₕ)Wₒ

where headᵢ = Attention(QWᵢq, KWᵢk, VWᵢv)

Typical: h=8 heads, dmodel=512, dhead=64
```

## Famous Transformer Models
- BERT (2018): Bidirectional encoder, masked language modeling
- GPT-2/3/4 (2019-2023): Autoregressive decoder, text generation
- T5 (2019): Encoder-decoder, unified text-to-text framework
- Vision Transformer (2020): applies transformers to image patches
- Whisper (2022): audio transformers for speech recognition
