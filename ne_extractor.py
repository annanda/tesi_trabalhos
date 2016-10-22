import nltk


class NEExtractor:
    def __init__(self, article_path):
        self.read_article(article_path)
        self.named_entities = []

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
            for word in sentence:
                if word[1] == 'NN' or word[1] == 'NNP':
                    if self.is_first_letter_upper(word[0]):
                        self.named_entities.append(word[0])

    def is_first_letter_upper(self, word):
        return word[0].isupper()

extractor = NEExtractor("documents/season_1/Baelor.txt")
extractor.get_ne(extractor.nominated_entities())
print(extractor.named_entities)
print(len(extractor.named_entities))
