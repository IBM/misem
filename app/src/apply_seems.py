import numpy
import pandas as pd
from pydantic import BaseModel
from sentence_transformers import util
from torch import softmax
import torch
from src.agglo_clustering import AggloClustering

from src.sentence_embedder import SentenceEmbedder
from src.token_embedder import TokenEmbedder
from sentence_transformers import SentenceTransformer
from typing import Any

sent_model = SentenceTransformer("all-mpnet-base-v2")


class SeemsResponse(BaseModel):
    seems_score: float
    reference_text_sentences: list
    inference_text_tokens: list
    cluster_labels: list
    x_tsne: list
    y_tsne: list
    z_tsne: list
    cluster_scores: list
    cluster_proportions: list
    cluster_affinity_matrix: list


def getScore(reference_text, inference_text, distance_threshold=0.9) -> SeemsResponse:
    reference_embedder = SentenceEmbedder(reference_text, sent_model)
    clustering = AggloClustering(
        reference_embedder.embeddings, distance_threshold)
    inference_embedder = TokenEmbedder(inference_text, sent_model)
    cluster_affinity_matrix = util.cos_sim(inference_embedder.embeddings.cpu(
    ), torch.stack([centroid.cpu() for centroid in clustering.cluster_centers]))
    soft_matrix = softmax(cluster_affinity_matrix, 1).T
    sum_stick = torch.sum(soft_matrix, 1)
    weighted_sum_stick = torch.dot(
        sum_stick, torch.tensor(clustering.cluster_proportions))
    norm_weighted_sum_stick = weighted_sum_stick / \
        len(inference_embedder.tokens)

    return SeemsResponse(seems_score=float(norm_weighted_sum_stick.item()),
                         reference_text_sentences=reference_embedder.sentences,
                         inference_text_tokens=inference_embedder.tokens,
                         cluster_labels=clustering.cluster_labels.tolist(),
                         x_tsne=clustering.x_tsne.tolist(),
                         y_tsne=clustering.y_tsne.tolist(),
                         z_tsne=clustering.z_tsne.tolist(),
                         cluster_scores=sum_stick.tolist(),
                         cluster_proportions=clustering.cluster_proportions,
                         cluster_affinity_matrix=cluster_affinity_matrix.tolist())
