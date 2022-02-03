class TokenEmbedder:
    """
    a class for embedding text with sentence embeddings
    """

    def __init__(self, text: str, model):
       
        self.text = text
        self.model = model.to(dev)
        self.sentences = self.__create_sentences()
        self.embeddings = self.__create_embeddings()
        self.tokens = self.__get_tokens()

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
            convert_to_tensor=True,
            output_value="token_embeddings"
        )
        return torch.cat(embeddings)

    def __get_tokens(self):
      ids_list = self.model.tokenizer(self.sentences)["input_ids"]
      tokens = []  # convert ids to tokens
      for ids in ids_list:
        tokens += self.model.tokenizer.convert_ids_to_tokens(ids)
      return tokens