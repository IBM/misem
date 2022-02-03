# IMPORTS

sent_model = SentenceTransformer("all-mpnet-base-v2")

def apply_seems(example_name, n_clusters=None):
  reference_path = f"/content/drive/MyDrive/SEEMS/SEEMSV2/Data/references_A_peer/{example_name}-A.txt"
  summaries_path = f"/content/drive/MyDrive/SEEMS/SEEMSV2/Data/summaries_A_peer/{example_name}-A.csv"


  with open(reference_path) as f:
    reference_text = f.readlines()
    reference_text = (" ").join(reference_text)

  reference_embedder = SentenceEmbedder(reference_text, sent_model)
  clustering = AggloClustering(reference_embedder.embeddings, n_clusters)

  summaries = pd.read_csv(summaries_path).sort_values(by="pyramid", ascending=False).reset_index(drop=True)

  seems_scores = []

  for index, row in summaries.iterrows():
    summary = row["summary"]
    inference_embedder = TokenEmbedder(summary, sent_model)
    cluster_affinity_matrix = util.cos_sim(inference_embedder.embeddings.cpu(), torch.stack([centroid.cpu() for centroid in clustering.cluster_centers]))
    soft_matrix =softmax(cluster_affinity_matrix, 1).T
    sum_stick = torch.sum(soft_matrix, 1)
    weighted_sum_stick = torch.dot(sum_stick, torch.tensor(clustering.cluster_proportions))
    norm_weighted_sum_stick = weighted_sum_stick / len(inference_embedder.tokens)
    seems_scores.append(norm_weighted_sum_stick.item())

  summaries["seems"] = seems_scores

  return summaries.corr(method="pearson")["pyramid"]["seems"]