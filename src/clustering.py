class Clustering(ABC):
    """
    Blueprint for clustering classes
    """

    def _get_cluster_centers(self):
        for i, embedding in enumerate(self.embeddings):
            cluster_index = self.cluster_labels[i]
            if cluster_index == None or cluster_index == -1:
                continue
            self.clusters[cluster_index].add_member(embedding, cluster_index)

        return [cluster.get_center() for cluster in self.clusters]

    def get_cluster_proportions(self):
        n = len(self.embeddings)
        return [len(cluster.members) / n for cluster in self.clusters]