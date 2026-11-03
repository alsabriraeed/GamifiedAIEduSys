# Slide 9: Attention Mechanisms

## What to Say (30-60 seconds)

Attention mechanisms were a game-changing innovation that addressed a key limitation of sequence models: they allow networks to focus on relevant parts of the input regardless of distance.

Here's the intuition: when translating "The cat sat on the mat" to French, translating "cat" requires looking back at "The" to decide if it's "le chat" or "la chatte." Attention explicitly computes relevance scores between all positions.

The mechanism works with three concepts: Query, Key, and Value. Think of it like searching: the Query is what you're looking for, Keys are indexed content, and Values are the actual information. We compute similarity between Query and all Keys, use this to weight the Values, and sum them up. This lets each position attend to all other relevant positions.

Self-attention is when queries, keys, and values all come from the same sequence - each word attending to all words. This captures relationships like subject-verb agreement, coreferences, and long-range dependencies that RNNs struggled with.

**Check Understanding:** How is attention different from RNN memory? Why can attention capture long-range dependencies better?

## Key Points
- Attention computes relevance between all input positions
- Query-Key-Value framework: search-like mechanism
- Self-attention: tokens attend to each other within same sequence
- Enables explicit modeling of long-range dependencies

## Common Student Questions

**Q: What exactly are Query, Key, and Value?**
A: All three are learned linear transformations of the input. Query = "what I'm looking for", Key = "what I have to offer", Value = "the actual information I provide". Attention = softmax(Q·Kᵀ)·V.

**Q: Why is it called attention?**
A: The weights computed from Query-Key similarity determine which Values to "pay attention to" - just like human attention focusing on relevant information.

**Q: How is this different from pooling or weighted averaging?**
A: The weights are dynamically computed based on content (Query-Key similarity), not fixed or position-based. Different queries produce different attention patterns.

**Q: What's the computational cost?**
A: O(n²) where n is sequence length - every position attends to every position. This is why very long sequences (>4096 tokens) become expensive. Efficient attention variants reduce this.

## Math Breakdown
```
Given input sequence: X ∈ ℝⁿˣᵈ

Linear projections:
Q = XWq  (queries)
K = XWk  (keys)  
V = XWv  (values)

Attention scores:
scores = QKᵀ / √dk  (scaled dot-product)

Attention weights:
α = softmax(scores)

Output:
Z = αV

Each position gets a weighted sum of all values,
weighted by query-key similarity.
```

## Visualization
Think of translating "The cat sat on the mat":
- When processing "sat", attention might:
  - Score high with "cat" (subject)
  - Score moderate with "The", "on", "mat"
  - Score low with other words
- Result: "sat" gets context-aware representation including "cat"
