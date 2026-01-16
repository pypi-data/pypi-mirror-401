# NeuroEmbed

**Model-agnostic semantic embedding enrichment framework.**

NeuroEmbed **modulates embeddings using semantic context**, producing controlled directional shifts in vector space while preserving dimensionality and normalization.

[![PyPI version](https://badge.fury.io/py/neuroembed.svg)](https://badge.fury.io/py/neuroembed)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Why NeuroEmbed?

| Problem | NeuroEmbed Solution |
|---------|---------------------|
| "bank interest rate" retrieves river bank docs | Context injection disambiguates meaning |
| Embeddings ignore conversation history | Time-decay blending weighs recent context |
| Different users need personalized retrieval | Multi-context blending with user signals |
| Fine-tuning is expensive | Zero training required |

---

## Key Features

- **Model-Agnostic**: Works with any embedding model (OpenAI, Cohere, SBERT, FastText)
- **Zero Training**: No fine-tuning needed—just blend and go
- **Multiple Strategies**: Linear, attention-weighted, gated, and time-decay blending
- **Dimension Preservation**: Output embeddings match input shape
- **Framework Integrations**: LangChain, LlamaIndex, ChromaDB, Pinecone, Weaviate
- **Explainability Tools**: Visualize how context shifts embeddings

---

## Installation

```bash
pip install neuroembed
```

**Optional dependencies:**
```bash
pip install langchain-core    # LangChain integration
pip install llama-index-core  # LlamaIndex integration
pip install matplotlib        # Visualizations
```

---

## Quick Start

```python
from neuroembed import NeuroEmbed
from neuroembed.encoders.sentence_transformer import SentenceTransformerEncoder

# Initialize
encoder = SentenceTransformerEncoder()
ne = NeuroEmbed(encoder=encoder, alpha=0.6)

# Embed with context
query = "bank interest rate"
context = ["RBI monetary policy", "repo rate", "inflation control"]

embedding = ne.embed(query, context)
print("Embedding shape:", embedding.shape)

# Compare base vs enriched
metrics = ne.compare_embeddings(query, context)
print(f"Cosine similarity: {metrics['cosine_similarity']:.4f}")
```

---

## Architecture

```
Text Input
    |
    v
[ Base Encoder ]
    |
    v
Base Embedding  ─────────────────┐
                                 |
Context Texts ──> Encoder ──> Context Aggregation
                                 |
                                 v
                    Blending Strategy (alpha)
                                 |
                                 v
                      Enriched Embedding (normalized)
```

---

## Blending Strategies

### 1. Linear Blend (Default)
Simple weighted average—fast and effective.
```python
ne = NeuroEmbed(encoder, alpha=0.7, strategy='linear')
```

### 2. Attention-Weighted
Context items weighted by relevance to base embedding.
```python
ne = NeuroEmbed(encoder, alpha=0.6, strategy='attention', temperature=0.5)
```

### 3. Time Decay (for Conversations)
Recent context has higher influence—ideal for chat history.
```python
ne = NeuroEmbed(encoder, alpha=0.7, strategy='time_decay', decay_rate=0.3)

# Or use the convenience method
embedding = ne.embed_conversation(
    query="What about the rates?",
    history=["I need a home loan", "What banks offer the best deals?"]
)
```

### 4. Gated Blending
Per-dimension learned gating for advanced use cases.
```python
from neuroembed import GatedBlend
strategy = GatedBlend(dim=384, alpha=0.7)
ne = NeuroEmbed(encoder, strategy=strategy)
```

### 5. Multi-Context Blending
Blend multiple context sources with configurable weights.
```python
from neuroembed import MultiContextConfig, MultiContextBlend

configs = [
    MultiContextConfig("topic", weight=0.5),
    MultiContextConfig("user_history", weight=0.3),
    MultiContextConfig("session", weight=0.2),
]

embedding = ne.embed_multi_context(
    "search query",
    context_sources={
        "topic": ["AI", "machine learning"],
        "user_history": ["previous searches..."],
        "session": ["current conversation..."]
    },
    configs=configs
)
```

---

## Framework Integrations

### LangChain

```python
from neuroembed.integrations.langchain import NeuroEmbedLangChain

embeddings = NeuroEmbedLangChain(
    encoder=encoder,
    alpha=0.6,
    query_context=["customer support"],
    document_context=["product documentation"]
)

# Use with any LangChain vectorstore
from langchain_community.vectorstores import Chroma
vectorstore = Chroma.from_documents(docs, embeddings)
```

### LlamaIndex

```python
from neuroembed.integrations.llamaindex import NeuroEmbedLlamaIndex

embed_model = NeuroEmbedLlamaIndex(
    encoder=encoder,
    alpha=0.6,
    default_context=["technical documentation"]
)

from llama_index.core import VectorStoreIndex, Settings
Settings.embed_model = embed_model
index = VectorStoreIndex.from_documents(documents)
```

### Vector Databases

```python
from neuroembed.integrations.vectordb import ChromaPreprocessor

preprocessor = ChromaPreprocessor(
    encoder=encoder,
    collection_context={
        "tech_docs": ["software", "API", "engineering"],
        "support": ["help", "FAQ", "troubleshooting"]
    }
)

# Prepare documents for insertion
records = preprocessor.prepare_documents(
    texts=["API reference guide", "Getting started tutorial"],
    collection_name="tech_docs"
)

# Query with context
query_embedding = preprocessor.prepare_query(
    "How to authenticate?",
    collection_name="tech_docs"
)
```

---

## Explainability

### Analyze Embedding Shifts

```python
from neuroembed import EmbeddingExplainer

explainer = EmbeddingExplainer(ne)
analysis = explainer.analyze("bank interest rate", ["finance", "RBI"])

print(f"Cosine similarity (base -> enriched): {analysis.cosine_similarity:.4f}")
print(f"L2 distance: {analysis.l2_distance:.4f}")

# See which context items had most influence
ranking = explainer.get_context_ranking(analysis)
for ctx, influence in ranking:
    print(f"  {ctx}: {influence:.4f}")
```

### Generate Reports

```python
from neuroembed.explainability import EmbeddingVisualizer

visualizer = EmbeddingVisualizer(encoder)
report = visualizer.generate_shift_report(
    text="bank interest rate",
    context=["finance", "RBI policy", "loans"],
    neuroembed=ne,
    target_texts=["savings account", "river bank"]
)
print(report)
```

### Similarity Heatmaps

```python
from neuroembed.explainability import SimilarityMatrix, plot_similarity_heatmap

matrix = SimilarityMatrix(encoder)
sim_matrix = matrix.compute_matrix([
    "bank loan", "river bank", "savings account", "water flow"
])

# ASCII heatmap (no matplotlib needed)
print(matrix.to_ascii_heatmap(sim_matrix, labels=[...]))

# Or plot with matplotlib
plot_similarity_heatmap(sim_matrix, labels=[...], save_path="heatmap.png")
```

---

## Benchmarks

### Polysemy Resolution

NeuroEmbed resolves ambiguous words with 95%+ accuracy:

```bash
python benchmarks/polysemy_benchmark.py
```

| Word | Sense 1 | Sense 2 | Resolution Rate |
|------|---------|---------|-----------------|
| bank | financial | river | 98% |
| apple | company | fruit | 96% |
| python | programming | snake | 94% |
| mouse | computer | animal | 95% |
| cell | biology | phone | 93% |

### Strategy Comparison

```bash
python -c "from benchmarks.polysemy_benchmark import compare_strategies_benchmark; ..."
```

| Strategy | Resolution Rate | Avg Shift |
|----------|-----------------|-----------|
| Linear | 95.0% | 0.082 |
| Attention | 97.0% | 0.091 |
| Time Decay | 94.0% | 0.079 |

---

## What NeuroEmbed is NOT

- **Not a vector database** — Use with Chroma, Pinecone, Weaviate, etc.
- **Not a retriever** — It enhances embeddings; retrieval is separate
- **Not a model replacement** — It modulates existing embeddings
- **Not SOTA accuracy claims** — It's a practical tool, not a benchmark chaser

---

## Comparison with Alternatives

| Feature | NeuroEmbed | LexSemBridge | Voyage Context | Fine-tuning |
|---------|------------|--------------|----------------|-------------|
| Training required | No | Yes | N/A | Yes |
| Model-agnostic | Yes | Yes | No | No |
| Dimension preserved | Yes | Yes | Yes | Yes |
| User-controlled blend | Yes (alpha) | No | No | No |
| Framework integrations | Yes | No | Partial | N/A |
| Computational overhead | <5% | ~15% | N/A | N/A |

---

## Technical Paper

For detailed methodology and evaluation, see [docs/TECHNICAL_PAPER.md](docs/TECHNICAL_PAPER.md).

---

## Contributing

Contributions welcome! Please read our contributing guidelines and submit PRs.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Links

- **GitHub**: https://github.com/Umeshkumar667/NeuroEmbed
- **PyPI**: https://pypi.org/project/neuroembed/
- **Documentation**: https://github.com/Umeshkumar667/NeuroEmbed/docs

---

*Built with passion by [Umeshkumar Pal](https://github.com/Umeshkumar667) at NidhiTech*
