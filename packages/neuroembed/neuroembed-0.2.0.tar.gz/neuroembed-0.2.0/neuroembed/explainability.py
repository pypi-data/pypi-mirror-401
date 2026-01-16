# neuroembed/explainability.py
"""
Explainability and visualization tools for NeuroEmbed.

Provides tools to understand and visualize how context affects embeddings:
- Cosine distance heatmaps
- PCA/t-SNE embedding projections
- Semantic shift analysis
- Context influence attribution
"""

import numpy as np
from typing import List, Dict, Optional, Tuple, Any, Union
from dataclasses import dataclass, field


@dataclass
class EmbeddingAnalysis:
    """Container for embedding analysis results."""
    base_embedding: np.ndarray
    enriched_embedding: np.ndarray
    context_embeddings: Optional[np.ndarray]
    context_texts: Optional[List[str]]
    
    # Computed metrics
    cosine_similarity: float = 0.0
    l2_distance: float = 0.0
    angular_distance: float = 0.0
    context_influences: Optional[List[float]] = None
    dimension_shifts: Optional[np.ndarray] = None
    
    def __post_init__(self):
        """Compute metrics after initialization."""
        self.cosine_similarity = float(
            self.base_embedding @ self.enriched_embedding /
            (np.linalg.norm(self.base_embedding) * np.linalg.norm(self.enriched_embedding))
        )
        self.l2_distance = float(np.linalg.norm(
            self.base_embedding - self.enriched_embedding
        ))
        self.angular_distance = float(np.arccos(
            np.clip(self.cosine_similarity, -1, 1)
        ))
        self.dimension_shifts = self.enriched_embedding - self.base_embedding
        
        if self.context_embeddings is not None and len(self.context_embeddings) > 0:
            # Compute per-context influence
            self.context_influences = [
                float(ctx @ self.enriched_embedding)
                for ctx in self.context_embeddings
            ]


class EmbeddingExplainer:
    """
    Explain how NeuroEmbed transforms embeddings with context.
    
    Provides detailed analysis of:
    - How much context shifts the base embedding
    - Which context items have most influence
    - Which dimensions are most affected
    - Similarity metrics before/after enrichment
    
    Example:
        explainer = EmbeddingExplainer(ne)
        analysis = explainer.analyze(
            "bank interest rate",
            ["finance", "RBI policy", "loans"]
        )
        print(analysis.cosine_similarity)
        print(analysis.context_influences)
    """
    
    def __init__(self, neuroembed):
        """
        Initialize explainer with a NeuroEmbed instance.
        
        Args:
            neuroembed: NeuroEmbed instance
        """
        self.ne = neuroembed
        self.encoder = neuroembed.encoder
    
    def analyze(
        self,
        text: str,
        context: Optional[List[str]] = None
    ) -> EmbeddingAnalysis:
        """
        Analyze embedding transformation.
        
        Args:
            text: Input text
            context: Context strings
        
        Returns:
            EmbeddingAnalysis with all computed metrics
        """
        result = self.ne.embed(text, context, return_components=True)
        
        return EmbeddingAnalysis(
            base_embedding=result["base"],
            enriched_embedding=result["enriched"],
            context_embeddings=result["context"],
            context_texts=result["context_texts"]
        )
    
    def compare_contexts(
        self,
        text: str,
        context_sets: Dict[str, List[str]]
    ) -> Dict[str, EmbeddingAnalysis]:
        """
        Compare embeddings with different context sets.
        
        Args:
            text: Input text
            context_sets: Dict mapping name -> context list
        
        Returns:
            Dict mapping name -> EmbeddingAnalysis
        """
        results = {}
        for name, context in context_sets.items():
            results[name] = self.analyze(text, context)
        return results
    
    def get_top_influenced_dimensions(
        self,
        analysis: EmbeddingAnalysis,
        top_k: int = 10
    ) -> List[Tuple[int, float]]:
        """
        Get dimensions most affected by context.
        
        Args:
            analysis: EmbeddingAnalysis object
            top_k: Number of top dimensions to return
        
        Returns:
            List of (dimension_index, shift_magnitude) tuples
        """
        shifts = np.abs(analysis.dimension_shifts)
        top_indices = np.argsort(shifts)[-top_k:][::-1]
        
        return [
            (int(idx), float(analysis.dimension_shifts[idx]))
            for idx in top_indices
        ]
    
    def get_context_ranking(
        self,
        analysis: EmbeddingAnalysis
    ) -> List[Tuple[str, float]]:
        """
        Rank context items by their influence on the enriched embedding.
        
        Args:
            analysis: EmbeddingAnalysis object
        
        Returns:
            List of (context_text, influence_score) sorted by influence
        """
        if analysis.context_texts is None or analysis.context_influences is None:
            return []
        
        ranked = list(zip(analysis.context_texts, analysis.context_influences))
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked


class SimilarityMatrix:
    """
    Build and visualize similarity matrices between embeddings.
    
    Useful for understanding how different texts/contexts relate
    in the embedding space.
    """
    
    def __init__(self, encoder):
        """
        Initialize with an encoder.
        
        Args:
            encoder: BaseEncoder instance
        """
        self.encoder = encoder
    
    def compute_matrix(
        self,
        texts: List[str],
        normalize: bool = True
    ) -> np.ndarray:
        """
        Compute pairwise similarity matrix.
        
        Args:
            texts: List of texts to compare
            normalize: Whether to L2 normalize embeddings
        
        Returns:
            Similarity matrix (n x n)
        """
        embeddings = self.encoder.encode(texts)
        
        if normalize:
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / norms
        
        return embeddings @ embeddings.T
    
    def compute_cross_matrix(
        self,
        texts_a: List[str],
        texts_b: List[str]
    ) -> np.ndarray:
        """
        Compute cross-similarity matrix between two text sets.
        
        Args:
            texts_a: First list of texts
            texts_b: Second list of texts
        
        Returns:
            Similarity matrix (len(a) x len(b))
        """
        emb_a = self.encoder.encode(texts_a)
        emb_b = self.encoder.encode(texts_b)
        
        # Normalize
        emb_a = emb_a / np.linalg.norm(emb_a, axis=1, keepdims=True)
        emb_b = emb_b / np.linalg.norm(emb_b, axis=1, keepdims=True)
        
        return emb_a @ emb_b.T
    
    def to_ascii_heatmap(
        self,
        matrix: np.ndarray,
        labels: Optional[List[str]] = None,
        width: int = 60
    ) -> str:
        """
        Convert matrix to ASCII heatmap string.
        
        Args:
            matrix: Similarity matrix
            labels: Optional row/column labels
            width: Maximum width of output
        
        Returns:
            ASCII representation of heatmap
        """
        chars = " .oO#"
        
        # Normalize to 0-1 range
        min_val = matrix.min()
        max_val = matrix.max()
        normalized = (matrix - min_val) / (max_val - min_val + 1e-8)
        
        lines = []
        n = matrix.shape[0]
        
        # Header
        if labels:
            max_label_len = min(10, max(len(l) for l in labels))
            header = " " * (max_label_len + 2)
            for i, label in enumerate(labels):
                header += label[:3].center(4)
            lines.append(header)
            lines.append("-" * len(header))
        
        # Rows
        for i in range(n):
            if labels:
                row = f"{labels[i][:max_label_len]:<{max_label_len}} |"
            else:
                row = f"{i:3d} |"
            
            for j in range(matrix.shape[1]):
                val = normalized[i, j]
                char_idx = min(int(val * len(chars)), len(chars) - 1)
                row += f" {chars[char_idx]}  "
            
            # Add numeric value for diagonal
            if i < matrix.shape[1]:
                row += f" | {matrix[i, i]:.2f}"
            
            lines.append(row)
        
        return "\n".join(lines)


class EmbeddingVisualizer:
    """
    Visualization utilities for embeddings.
    
    Provides PCA, t-SNE projections and other visualizations.
    Note: For actual plotting, matplotlib/plotly is optional.
    This class provides the data structures needed for visualization.
    """
    
    def __init__(self, encoder):
        """
        Initialize with an encoder.
        
        Args:
            encoder: BaseEncoder instance
        """
        self.encoder = encoder
    
    def pca_projection(
        self,
        embeddings: np.ndarray,
        n_components: int = 2
    ) -> np.ndarray:
        """
        Project embeddings to lower dimensions using PCA.
        
        Args:
            embeddings: Array of embeddings (n x dim)
            n_components: Number of components (2 or 3)
        
        Returns:
            Projected embeddings (n x n_components)
        """
        # Center the data
        centered = embeddings - np.mean(embeddings, axis=0)
        
        # Compute covariance and eigendecomposition
        cov = np.cov(centered.T)
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        
        # Sort by eigenvalue (descending)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvectors = eigenvectors[:, idx]
        
        # Project
        projection = centered @ eigenvectors[:, :n_components]
        return projection
    
    def compute_shift_trajectory(
        self,
        text: str,
        context: List[str],
        neuroembed,
        alpha_steps: List[float] = None
    ) -> Dict[str, Any]:
        """
        Compute embedding trajectory as alpha varies.
        
        Args:
            text: Input text
            context: Context strings
            neuroembed: NeuroEmbed instance
            alpha_steps: Alpha values to evaluate
        
        Returns:
            Dict with trajectory data
        """
        if alpha_steps is None:
            alpha_steps = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        
        base_emb = self.encoder.encode([text])[0]
        ctx_embs = self.encoder.encode(context)
        ctx_mean = np.mean(ctx_embs, axis=0)
        
        embeddings = []
        similarities = []
        
        for alpha in alpha_steps:
            enriched = alpha * base_emb + (1 - alpha) * ctx_mean
            enriched = enriched / np.linalg.norm(enriched)
            embeddings.append(enriched)
            similarities.append(float(base_emb @ enriched))
        
        return {
            "alpha_steps": alpha_steps,
            "embeddings": np.array(embeddings),
            "base_similarities": similarities,
            "base_embedding": base_emb,
            "context_mean": ctx_mean
        }
    
    def generate_shift_report(
        self,
        text: str,
        context: List[str],
        neuroembed,
        target_texts: Optional[List[str]] = None
    ) -> str:
        """
        Generate a text report of embedding shift analysis.
        
        Args:
            text: Input text
            context: Context strings
            neuroembed: NeuroEmbed instance
            target_texts: Optional target texts to compare similarity
        
        Returns:
            Formatted text report
        """
        explainer = EmbeddingExplainer(neuroembed)
        analysis = explainer.analyze(text, context)
        
        lines = [
            "=" * 60,
            "NEUROEMBED SHIFT ANALYSIS REPORT",
            "=" * 60,
            "",
            f"Input Text: \"{text}\"",
            f"Context Items: {len(context) if context else 0}",
            "",
            "-" * 60,
            "SIMILARITY METRICS",
            "-" * 60,
            f"  Cosine Similarity (base -> enriched): {analysis.cosine_similarity:.4f}",
            f"  L2 Distance: {analysis.l2_distance:.4f}",
            f"  Angular Distance: {np.degrees(analysis.angular_distance):.2f} deg",
            "",
        ]
        
        # Context influence
        if context and analysis.context_influences:
            lines.extend([
                "-" * 60,
                "CONTEXT INFLUENCE RANKING",
                "-" * 60,
            ])
            ranking = explainer.get_context_ranking(analysis)
            for i, (ctx_text, influence) in enumerate(ranking, 1):
                lines.append(f"  {i}. \"{ctx_text[:40]}...\" -> {influence:.4f}")
            lines.append("")
        
        # Top shifted dimensions
        lines.extend([
            "-" * 60,
            "TOP 5 SHIFTED DIMENSIONS",
            "-" * 60,
        ])
        top_dims = explainer.get_top_influenced_dimensions(analysis, top_k=5)
        for dim_idx, shift in top_dims:
            direction = "+" if shift > 0 else "-"
            lines.append(f"  Dim {dim_idx:4d}: {direction} {abs(shift):.4f}")
        lines.append("")
        
        # Target similarities if provided
        if target_texts:
            lines.extend([
                "-" * 60,
                "TARGET SIMILARITY COMPARISON",
                "-" * 60,
            ])
            target_embs = self.encoder.encode(target_texts)
            for target_text, target_emb in zip(target_texts, target_embs):
                base_sim = float(analysis.base_embedding @ target_emb)
                enriched_sim = float(analysis.enriched_embedding @ target_emb)
                delta = enriched_sim - base_sim
                direction = "+" if delta > 0 else "-"
                lines.append(
                    f"  \"{target_text[:30]}...\"\n"
                    f"    Base: {base_sim:.4f} -> Enriched: {enriched_sim:.4f} "
                    f"({direction}{abs(delta):.4f})"
                )
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


def plot_similarity_heatmap(
    matrix: np.ndarray,
    labels: List[str],
    title: str = "Similarity Heatmap",
    save_path: Optional[str] = None
) -> Any:
    """
    Plot a similarity heatmap using matplotlib.
    
    Args:
        matrix: Similarity matrix
        labels: Row/column labels
        title: Plot title
        save_path: Optional path to save figure
    
    Returns:
        matplotlib figure (or None if matplotlib unavailable)
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
    except ImportError:
        print("matplotlib not available. Install with: pip install matplotlib")
        return None
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto')
    
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_yticklabels(labels)
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Cosine Similarity", rotation=-90, va="bottom")
    
    # Add text annotations
    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(
                j, i, f"{matrix[i, j]:.2f}",
                ha="center", va="center", color="black", fontsize=8
            )
    
    ax.set_title(title)
    fig.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def plot_embedding_pca(
    embeddings: np.ndarray,
    labels: List[str],
    colors: Optional[List[str]] = None,
    title: str = "Embedding PCA Projection",
    save_path: Optional[str] = None
) -> Any:
    """
    Plot 2D PCA projection of embeddings.
    
    Args:
        embeddings: Array of embeddings
        labels: Text labels for each point
        colors: Optional color for each point
        title: Plot title
        save_path: Optional path to save figure
    
    Returns:
        matplotlib figure (or None if matplotlib unavailable)
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available. Install with: pip install matplotlib")
        return None
    
    visualizer = EmbeddingVisualizer(None)
    projected = visualizer.pca_projection(embeddings, n_components=2)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if colors is None:
        colors = ['#3498db'] * len(labels)
    
    scatter = ax.scatter(
        projected[:, 0], projected[:, 1],
        c=range(len(labels)), cmap='viridis',
        s=100, alpha=0.7
    )
    
    for i, label in enumerate(labels):
        ax.annotate(
            label[:20],
            (projected[i, 0], projected[i, 1]),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=8
        )
    
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig
