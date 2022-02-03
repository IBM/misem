class AggloClustering(Clustering):
    """"""

    def __init__(self, embeddings, distance_threshold=10):
        """
        :param embeddings: list of tensors
        :param tokens_list: list of tokens
        :param distance_threshold:
        """
        self.embeddings = embeddings
        self.cluster_output = AgglomerativeClustering(
           n_clusters=None, distance_threshold=distance_threshold,
        affinity="cosine", linkage="complete").fit(self.embeddings.cpu().numpy())
        self.cluster_labels = self.cluster_output.labels_
        self.n_cluster = len(set(filter(lambda x: x != -1, self.cluster_labels)))
        percentage = len(list(filter(lambda x: x != -1, self.cluster_labels))) / len(
            self.embeddings
        )

        self.clusters = []

        # self.cluster_output.n_clusters_ = len(set(self.cluster_output.labels_))
        self.clusters = [Cluster(i) for i in range(self.n_cluster)]
        self.cluster_centers = self._get_cluster_centers()
        self.cluster_proportions = self.get_cluster_proportions()