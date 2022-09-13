import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000/seems/score"

@st.cache(show_spinner=False)
def get_seems(reference_text: str, inference_text: str, distance_threshold: float = 0.9):
    """
    Get data from SEEMS backend using POST request
    The data is returned as a json object, which includes the following keys:
    - seems_score: float value
    - reference_text_sentences: list of sentences in the reference text
    - inference_text_tokens: list of tokens in the inference text
    - cluster_labels: list of cluster labels
    - x_tsne: list of x-coordinates for t-SNE
    - y_tsne: list of y-coordinates for t-SNE
    - z_tsne: list of z-coordinates for t-SNE
    - cluster_scores: cluster scores
    - cluster_proportions: proportions of each cluster
    - cluster_affinity_matrix: cluster affinity scores for each token in the inference text
    """

    # generate fake data for testing
    # response = {
    #     "seems_score": 0.5,
    #     "reference_text_sentences": [
    #         "The quick brown fox jumps over the lazy dog.",
    #         "The quick brown fox jumps over the lazy dog.",
    #         "The quick brown fox jumps over the lazy dog.",
    #         "The quick brown fox jumps over the lazy dog.",
    #     ],
    #     "inference_text_tokens": [
    #         "A",
    #         "fast",
    #         "brown",
    #         "dog",
    #         "walked",
    #     ],
    #     "cluster_labels": [0, 0, 1, 2],
    #     "x_tsne": [0.0, 0.0, 0.0, 0.0],
    #     "y_tsne": [0.0, 0.0, 0.0, 0.0],
    #     "z_tsne": [0.0, 0.0, 0.0, 0.0],
    #     "cluster_scores": [1000, 500, 350],
    #     "cluster_proportions": [0.5, 0.25, 0.25],
    #     "cluster_affinity_matrix": [
    #         [0.6, 0.55, 0.7, 0.2, 0.1],
    #         [0.2, 0.3, 0.3, 0.57, 0.6],
    #         [0.4, 0.8, 0.6, 0.2, 0.5]
    #     ]
    # }

    data = {
        "ref_text": reference_text,
        "inf_text": inference_text,
        "distance_threshold": distance_threshold,
    }

    response = requests.post(BASE_URL, json=data)

    return response.json()