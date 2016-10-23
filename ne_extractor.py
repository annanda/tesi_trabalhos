import nltk


class NEExtractor:
    def __init__(self, article_path):
        self.read_article(article_path)
        self.named_entities = []
        self.get_ne(self.nominated_entities())
        self.create_ne_file()

    def nominated_entities(self):

        sentences = nltk.sent_tokenize(self.article)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

        return tagged_sentences

    def read_article(self, path):
        with open(path, 'r') as article:
            self.article = article.read()

    def get_ne(self, tagged_sentences):
        for sentence in tagged_sentences:
            anterior_is_ne = False
            for word in sentence:
                if self.is_nnp_and_upper(word[0], word[1]):
                    if anterior_is_ne:
                        self.named_entities[-1] = self.named_entities[-1] + " " + word[0]
                    else:
                        self.named_entities.append(word[0])
                    anterior_is_ne = True
                else:
                    anterior_is_ne = False

    def is_first_letter_upper(self, word):
        return word[0].isupper()

    def is_nnp_and_upper(self, word, tag):
        if tag == 'NN' or tag == 'NNP':
            if self.is_first_letter_upper(word):
                return True
        return False

    def create_ne_file(self):
        # para nao repetir os elementos
        self.named_entities = set(self.named_entities)
        self.named_entities = list(self.named_entities)
        self.named_entities.sort()
        with open("entidades_nomeadas.csv", 'w') as article_file:
            for entidade in self.named_entities:
                article_file.write(entidade + "\n")

extractor = NEExtractor("second_processing/Baelor s1e9.txt")

# primeira tentativa de extrair entidades nomeadas no arquivo Baelor.txt
# 873 entidades nomeadas

# segunda tentativa: transformando de lista pra conjunto
# 319 entidades nomeadas

# terceira tentativa: colocando ne seguidas como uma só
# 336 entidades nomeadas
# muitas substrings repetidas

#quarta tentativa: mudando o pre-processamento
# apenas com as secoes: Plot, Summary, Appearances and Deaths
# 113 endidades nomeadas

# quinta tentativa: consertando o metodo que junta mais de uma NE seguidas
# 105 entidades nomeadas