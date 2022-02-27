from request.seems_backend import get_seems
from request.gpt import get_topic

class SEEMSController:
    def __init__(self):
        self.reference_text = None
        self.inference_text = None
        self.distance_threshold = None
        self.seems_score = None
        self.reference_text_sentences = None
        self.inference_text_tokens = None
        self.cluster_labels = None
        self.x_tsne = None
        self.y_tsne = None
        self.z_tsne = None
        self.cluster_scores = None
        self.cluster_proportions = None
        self.cluster_affinity_matrix = None
        self.topic = None

    def get_results(self, reference_text: str, inference_text: str, distance_threshold: float = 0.9):
        self.reference_text = reference_text
        self.inference_text = inference_text
        self.distance_threshold = distance_threshold
        results = get_seems(self.reference_text, self.inference_text, self.distance_threshold)
        self.seems_score = results["seems_score"]
        self.reference_text_sentences = results["reference_text_sentences"]
        self.inference_text_tokens = results["inference_text_tokens"]
        self.cluster_labels = results["cluster_labels"]
        self.x_tsne = results["x_tsne"]
        self.y_tsne = results["y_tsne"]
        self.z_tsne = results["z_tsne"]
        self.cluster_scores = results["cluster_scores"]
        self.cluster_proportions = results["cluster_proportions"]
        self.cluster_affinity_matrix = results["cluster_affinity_matrix"]

    def __str__(self):
        return f"""
        SEEMS Score: {self.seems_score}
        Reference Text Sentences: {self.reference_text_sentences}
        Inference Text Tokens: {self.inference_text_tokens}
        Cluster Labels: {self.cluster_labels}
        X-t-SNE: {self.x_tsne}
        Y-t-SNE: {self.y_tsne}
        Z-t-SNE: {self.z_tsne}
        Cluster Scores: {self.cluster_scores}
        Cluster Proportions: {self.cluster_proportions}
        Cluster Affinity Matrix: {self.cluster_affinity_matrix}
        """

class TopicController:
    def __init__(self, sentences: list, cluster_labels: list):
        self.sentences = sentences
        self.cluster_labels = cluster_labels
        self.clustered_sentences_dict = self.__merge_sentences_by_cluster(self.cluster_labels, self.sentences)
        self.clustered_sentences_dict = self.__convert_values_to_text(self.clustered_sentences_dict)

    def __merge_sentences_by_cluster(self, cluster_labels: list, sentences: list) -> dict:
        '''
        Returns a dictionary of lists of strings, where the keys are the cluster labels and the values are the sentences.
        input:
            cluster_labels: list of strings
            sentences: list of strings
        output:
            clustered_sentences_dict: dictionary of lists of strings
        '''

        clustered_sentences_dict = {}

        for cluster_label, sentence in zip(cluster_labels, sentences):
            if cluster_label not in clustered_sentences_dict:
                clustered_sentences_dict[cluster_label] = []
            clustered_sentences_dict[cluster_label].append(sentence)

        return clustered_sentences_dict

    def __convert_values_to_text(self, clustered_sentences_dict: dict) -> dict:
        '''
        Returns a dictionary of strings, where the keys are the cluster labels and the values are the sentences.
        input:
            clustered_sentences_dict: dictionary of lists of strings
        output:
            clustered_sentences_dict: dictionary of strings
        '''

        for key, value in clustered_sentences_dict.items():
            clustered_sentences_dict[key] = " ".join(value)

        return clustered_sentences_dict

    def get_topics(self) -> list:
        '''
        Returns a list of strings, where each string is a topic.
        input:
            clustered_sentences_dict: dictionary of strings
        output:
            topics: list of strings
        '''

        topics = []

        for key, value in self.clustered_sentences_dict.items():
            topics.append(get_topic(value))

        return topics
