import nltk


class NEExtractor:
    def __init__(self, article_path):
        self.read_article(article_path)

    def nominated_entities(self):

        sentences = nltk.sent_tokenize(self.article)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

        return tagged_sentences

    def read_article(self, path):
        with open(path, 'r') as article:
            self.article = article.read()


extractor = NEExtractor("documents/season_1/Baelor.txt")
print(extractor.nominated_entities())