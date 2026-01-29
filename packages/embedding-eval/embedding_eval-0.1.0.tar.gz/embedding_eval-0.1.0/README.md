# embedding-eval

Fair embedding model evaluation with independent parameter optimization.

## Why This Package?

Most embedding comparisons are unfair because they use the same parameters for all models. This package implements a fair comparison methodology:

| Approach | Description | Fair? |
|----------|-------------|-------|
| **Unfair** | Optimize parameters for Model A, apply to all models | ❌ |
| **Fair** | Each model gets its own optimized parameters | ✅ |

## Key Features

- **Independent Optimization**: Each model gets its own best `chunk_size`, `overlap`, and `top_k`
- **Binary Evaluation**: Simple substring matching, no LLM cost, reproducible
- **Confidence Intervals**: Reports 95% CI using Wilson score
- **Minimal Dependencies**: Core functionality requires only `sentence-transformers` and `tiktoken`
- **No External Services**: InMemoryVectorStore requires no database setup

## Installation

```bash
pip install embedding-eval

# For OpenAI models
pip install embedding-eval[openai]
```

## Quick Start

```python
from embedding_eval import run_fair_comparison

# Your document content
doc_content = open("document.txt").read()

# Q&A pairs where answers appear VERBATIM in the document
qa_pairs = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "When was the company founded?", "answer": "1995"},
    # ... more pairs (recommend 80+ for statistical power)
]

# Compare models with independent optimization
results = run_fair_comparison(
    models=["st:bge-base", "st:minilm"],
    doc_content=doc_content,
    qa_pairs=qa_pairs,
)

# Results include baseline + optimized + confidence intervals
for r in results:
    print(f"{r.model_name}:")
    print(f"  Baseline: {r.baseline_accuracy:.1f}%")
    print(f"  Optimized: {r.best_accuracy:.1f}% (95% CI: [{r.ci_lower:.1f}%, {r.ci_upper:.1f}%])")
    print(f"  Best params: {r.best_params}")
```

## Methodology

### Fair Comparison = Independent Optimization

```
┌────────────────────────────────────────────────────────────────┐
│  FAIR COMPARISON METHODOLOGY                                   │
│                                                                │
│  For each model:                                               │
│    1. Grid search over chunk_size × overlap × top_k            │
│    2. Find best parameters for THIS model                      │
│    3. Report: baseline + optimized + 95% CI                    │
│                                                                │
│  Compare models using their respective best configurations     │
└────────────────────────────────────────────────────────────────┘
```

### Binary Evaluation

We use substring matching to check if the expected answer appears in retrieved chunks:

```python
from embedding_eval import BinaryEvaluator

evaluator = BinaryEvaluator()
score = evaluator.evaluate(
    question="What is the capital?",
    expected_answer="Paris",
    retrieved_chunks=["France is a country. Paris is its capital."]
)
print(score.score)  # 1.0 (answer found)
```

**Why binary evaluation?**
- Simple and reproducible
- No LLM cost ($0 vs ~$0.03/question for LLM evaluation)
- Proven effective for parameter optimization (see EDD-005)
- RAGAS and LLM evaluation add cost without improving decisions

### Statistical Requirements

| Sample Size | 95% CI Width | Can Detect |
|-------------|--------------|------------|
| 50 | ±11% | >22% differences |
| 80 | ±9% | >18% differences |
| 100 | ±8% | >16% differences |

**Recommendation**: Use 80+ questions with 20%+ multi-hop for meaningful comparisons.

## Q&A Fixture Format

```json
[
  {
    "question": "What does BATNA stand for?",
    "answer": "Best Alternative To a Negotiated Agreement",
    "category": "exact",
    "difficulty": "medium"
  }
]
```

**Important**: Answers must appear **verbatim** in the document.

## Model Specifications

| Format | Example | Description |
|--------|---------|-------------|
| `st:<model>` | `st:bge-base` | SentenceTransformers (free, local) |
| `openai:<model>` | `openai:text-embedding-3-small` | OpenAI API (requires key) |

### Recommended Models

| Use Case | Model | Accuracy | Cost |
|----------|-------|----------|------|
| **Best value** | `st:bge-base` | 94.4% | Free |
| Quality-first | `openai:text-embedding-3-small` | 97.3% | ~$0.02/1M tokens |
| Fast prototyping | `st:minilm` | 89.7% | Free |

## API Reference

### Core Functions

```python
# Compare multiple models
from embedding_eval import run_fair_comparison
results = run_fair_comparison(
    models=["st:bge-base", "st:minilm"],
    doc_content=text,
    qa_pairs=pairs,
    chunk_sizes=[256, 384, 512],  # optional
    overlaps=[25, 50, 100],       # optional
    top_ks=[5, 10, 15],           # optional
)

# Optimize single model
from embedding_eval import optimize_model
result = optimize_model(
    model_spec="st:bge-base",
    doc_content=text,
    qa_pairs=pairs,
)
```

### Components

```python
# Chunking
from embedding_eval.chunking import FixedSizeChunker
chunker = FixedSizeChunker(chunk_size=512, overlap=50)
chunks = chunker.chunk(document)

# Embedding
from embedding_eval.adapters.embedding import SentenceTransformerEmbedding
embedding = SentenceTransformerEmbedding(model="bge-base")
vectors = embedding.embed_documents(texts)

# Vector Store (no external deps)
from embedding_eval.adapters.vector import InMemoryVectorStore
store = InMemoryVectorStore()
store.connect()
store.create_collection("test", dimensions=768)
store.upsert("test", ids, embeddings, texts=texts)
results = store.search("test", query_embedding, top_k=10)

# Evaluation
from embedding_eval import BinaryEvaluator
evaluator = BinaryEvaluator()
score = evaluator.evaluate(question, answer, chunks)
```

## Key Research Findings

Based on comprehensive evaluation (712 questions across 5 document types):

1. **Chunking matters most**: Section-aware chunking improved Q33 from rank 66 → rank 2 (more impact than any algorithm change)

2. **Recommended configuration**:
   ```python
   config = {
       "chunk_size": 512,
       "overlap": 50,
       "top_k": 10,
   }
   # Accuracy: 94.0% with BGE-base
   ```

3. **What NOT to do**:
   - Graph retrieval causes -4.6% to -4.9% regression on most documents
   - Small chunks (128 tokens) generalize poorly
   - Query expansion helps vocabulary mismatch but can hurt precision

## License

MIT

## Contributing

Contributions welcome! Please open an issue first to discuss proposed changes.
