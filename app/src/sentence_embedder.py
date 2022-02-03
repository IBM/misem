
import numpy as np
import torch
from spacy.lang.en import English
if torch.cuda.is_available():
    dev = "cuda:0"
else:
    dev = "cpu"


class SentenceEmbedder:
    """
    a class for embedding text with sentence embeddings
    """

    def __init__(self, text: str, model):

        self.text = text
        self.model = model.to(dev)
        self.sentences = self.__create_sentences()
        self.embeddings = self.__create_embeddings()

    def __create_sentences(self):

        nlp = English()
        nlp.add_pipe("sentencizer")
        doc = nlp(str(self.text))
        return [sentence.text for sentence in doc.sents]

    def __create_embeddings(self):

        # convert token to windows of tokens
        embeddings = self.model.encode(
            sentences=self.sentences,
            show_progress_bar=False,
            normalize_embeddings=True,
            convert_to_tensor=True
        )

        return embeddings
