import streamlit as st
from annotated_text import annotated_text
from matplotlib.colors import to_hex
import matplotlib.pyplot as plt

class Annotator:
    """
    params:
        token_list: list of inference text tokens
        affinity_matrix: cosine similarity matrix between tokens and clusters
    """

    def __init__(self, inference_tokens: list, reference_sentences: list, affinity_matrix, cluster_labels: list):
        self.tokens = inference_tokens
        self.reference_sentences = reference_sentences
        self.affinity_matrix = affinity_matrix
        self.cluster_labels = cluster_labels

    def __get_cluster_token_similarities(self, cluster_label: int) -> list:
        """
        Returns a dictionary of lists of floats, where the keys are the cluster labels and the values are the similarity scores between tokens and clusters.
        input:
            affinity_matrix: cosine similarity matrix between tokens and clusters
        output:
            cluster_token_similarities: list of floats
        """

        return self.affinity_matrix[cluster_label]

    def __get_annotation_tuples(self, cluster_label: int):
        """
        Returns a list of tuples, where each tuple is a token, its similarity score to the cluster and its color.
        input:
            cluster_label: int
        output:
            annotations: list of tuples
        """

        cluster_token_similarities = self.__get_cluster_token_similarities(cluster_label)

        color_map = plt.cm.get_cmap('plasma', len(cluster_token_similarities))

        annotations = []

        for token, similarity in zip(self.tokens, cluster_token_similarities):
            color = color_map(similarity)
            # convert the color from rgba to hex
            color = to_hex(color)
            annotations.append((token, similarity, color))

        return annotations

    def __apply_threshold(self, cluster_label: int, threshold: float = 0.5):
        """
        Returns a list of tuples, where each tuple is a token, its similarity score to the cluster and its color, if the similarity score is greater than the threshold. Else, only the token is returned.
        input:
            cluster_label: int
            threshold: float
        output:
            annotations: list of tuples/ strings
        """

        annotations = self.__get_annotation_tuples(cluster_label)

        # if the similarity score is above the threshold, keep the tuple, otherwise, only keep the token

        annotated_text_list = []

        for token, similarity, color in annotations:
            if similarity > threshold:
                annotated_text_list.append((token, str(similarity), color))
            else:
                annotated_text_list.append(" " + token + " ")

        return annotated_text_list

    def get_annotated_inference_text(self, cluster_label: int, threshold: float = 0.5):
        """
        Returns a list of tuples, where each tuple is a token, its similarity score to the cluster and its color, if the similarity score is greater than the threshold. Else, only the token is returned.
        input:
            cluster_label: int
            threshold: float
        output:
            annotations: list of tuples/ strings
        """

        return annotated_text(*self.__apply_threshold(cluster_label, threshold))

    def get_annotated_reference_text(self, cluster_label: int, color: str = '#E6EE9C'):
        """
        Returns a list of tuples, where each tuple is a sentence, and its color, based on the cluster_label.
        input:
            cluster_label: int
        output:
            annotations: list of tuples/ strings
        """

        annotations = []

        for i, sentence in enumerate(self.reference_sentences):
            annotations.append((sentence, str(cluster_label), color) if self.cluster_labels[i] == cluster_label else " " + sentence + " ")

        return annotated_text(*annotations)