# tests/test_explainability.py
"""
Tests for explainability and visualization tools.
"""

import numpy as np
import pytest
from neuroembed import NeuroEmbed
from neuroembed.encoders.sentence_transformer import SentenceTransformerEncoder
from neuroembed.explainability import (
    EmbeddingAnalysis,
    EmbeddingExplainer,
    EmbeddingVisualizer,
    SimilarityMatrix,
)


@pytest.fixture(scope="module")
def encoder():
    return SentenceTransformerEncoder()


@pytest.fixture(scope="module")
def ne(encoder):
    return NeuroEmbed(encoder=encoder, alpha=0.6)


class TestEmbeddingAnalysis:
    def test_analysis_computes_metrics(self, encoder):
        base = encoder.encode(["test"])[0]
        context = encoder.encode(["context1", "context2"])
        
        # Simulate enriched embedding
        enriched = 0.7 * base + 0.3 * np.mean(context, axis=0)
        enriched = enriched / np.linalg.norm(enriched)
        
        analysis = EmbeddingAnalysis(
            base_embedding=base,
            enriched_embedding=enriched,
            context_embeddings=context,
            context_texts=["context1", "context2"]
        )
        
        assert 0 < analysis.cosine_similarity <= 1
        assert analysis.l2_distance >= 0
        assert analysis.angular_distance >= 0
        assert analysis.dimension_shifts is not None
        assert len(analysis.context_influences) == 2


class TestEmbeddingExplainer:
    def test_analyze(self, ne):
        text = "bank interest rate"
        context = ["finance", "loans", "banking"]
        
        explainer = EmbeddingExplainer(ne)
        analysis = explainer.analyze(text, context)
        
        assert isinstance(analysis, EmbeddingAnalysis)
        assert analysis.cosine_similarity > 0
    
    def test_compare_contexts(self, ne):
        text = "bank"
        context_sets = {
            "finance": ["money", "loans"],
            "river": ["water", "nature"],
        }
        
        explainer = EmbeddingExplainer(ne)
        results = explainer.compare_contexts(text, context_sets)
        
        assert "finance" in results
        assert "river" in results
        assert isinstance(results["finance"], EmbeddingAnalysis)
    
    def test_get_top_influenced_dimensions(self, ne):
        explainer = EmbeddingExplainer(ne)
        analysis = explainer.analyze("test", ["context"])
        
        top_dims = explainer.get_top_influenced_dimensions(analysis, top_k=5)
        
        assert len(top_dims) == 5
        assert all(isinstance(d, tuple) and len(d) == 2 for d in top_dims)
    
    def test_get_context_ranking(self, ne):
        explainer = EmbeddingExplainer(ne)
        analysis = explainer.analyze("test", ["context1", "context2", "context3"])
        
        ranking = explainer.get_context_ranking(analysis)
        
        assert len(ranking) == 3
        # Should be sorted by influence (descending)
        influences = [r[1] for r in ranking]
        assert influences == sorted(influences, reverse=True)


class TestSimilarityMatrix:
    def test_compute_matrix(self, encoder):
        texts = ["hello", "hi", "goodbye"]
        
        matrix = SimilarityMatrix(encoder)
        sim_matrix = matrix.compute_matrix(texts)
        
        assert sim_matrix.shape == (3, 3)
        # Diagonal should be 1 (self-similarity)
        assert np.allclose(np.diag(sim_matrix), 1.0, atol=1e-6)
        # Matrix should be symmetric
        assert np.allclose(sim_matrix, sim_matrix.T)
    
    def test_compute_cross_matrix(self, encoder):
        texts_a = ["cat", "dog"]
        texts_b = ["animal", "pet", "vehicle"]
        
        matrix = SimilarityMatrix(encoder)
        cross_matrix = matrix.compute_cross_matrix(texts_a, texts_b)
        
        assert cross_matrix.shape == (2, 3)
    
    def test_to_ascii_heatmap(self, encoder):
        texts = ["cat", "dog"]
        
        matrix = SimilarityMatrix(encoder)
        sim_matrix = matrix.compute_matrix(texts)
        
        ascii_map = matrix.to_ascii_heatmap(sim_matrix, labels=texts)
        
        assert isinstance(ascii_map, str)
        assert len(ascii_map) > 0


class TestEmbeddingVisualizer:
    def test_pca_projection(self, encoder):
        embeddings = encoder.encode(["cat", "dog", "car", "truck"])
        
        visualizer = EmbeddingVisualizer(encoder)
        projected = visualizer.pca_projection(embeddings, n_components=2)
        
        assert projected.shape == (4, 2)
    
    def test_compute_shift_trajectory(self, encoder, ne):
        visualizer = EmbeddingVisualizer(encoder)
        
        trajectory = visualizer.compute_shift_trajectory(
            text="bank",
            context=["finance", "money"],
            neuroembed=ne,
            alpha_steps=[0.0, 0.5, 1.0]
        )
        
        assert "alpha_steps" in trajectory
        assert "embeddings" in trajectory
        assert "base_similarities" in trajectory
        assert len(trajectory["embeddings"]) == 3
    
    def test_generate_shift_report(self, encoder, ne):
        visualizer = EmbeddingVisualizer(encoder)
        
        report = visualizer.generate_shift_report(
            text="bank",
            context=["finance", "loans"],
            neuroembed=ne
        )
        
        assert isinstance(report, str)
        assert "NEUROEMBED" in report
        assert "Cosine Similarity" in report
