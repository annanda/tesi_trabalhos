import nltk
import re
import glob
import os.path

class NEExtractor:

    named_entities = []

    def __init__(self, article_path):
        self.article = self.read_article(article_path)
        self.get_ne(self.nominated_entities())
        # self.create_ne_file()
        # self.read_test_file()

    def nominated_entities(self):

        sentences = re.split(r'[\.\n]', self.article)
        sentences = [sentence.strip(" '") for sentence in sentences]
        sentences = [sentence for sentence in sentences if sentence]

        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

        return tagged_sentences

    def read_article(self, path):
        with open(path, 'r', encoding="utf-8") as article:
            return article.read()

    def get_ne(self, tagged_sentences):
        ne = []
        for i, sentence in enumerate(tagged_sentences):
            for j, tagged_word in enumerate(sentence):

                if self.is_first_letter_upper(tagged_word):
                    if self.is_first_word_and_not_np(j, tagged_word):
                        continue
                    ne.append(tagged_word)
                    continue

                if ne and self.is_complement(tagged_word):
                    ne.append(tagged_word)
                    continue

                if ne:
                    if self.has_np(ne):
                        ne = self.remove_unfinished_complements(ne)
                        named_entity = self.build_named_entity(ne)
                        # print("({2}){0} - {1}\n".format(named_entity, str(sentence), i))
                        self.named_entities.append(named_entity)

                    ne.clear()
            if ne:
                if self.has_np(ne):
                    ne = self.remove_unfinished_complements(ne)
                    named_entity = self.build_named_entity(ne)
                    # print("({2}){0} - {1}\n".format(named_entity, str(sentence), i))
                    self.named_entities.append(named_entity)

                ne.clear()

    def build_named_entity(self, ne):
        named_entity = " ".join([word[0] for word in ne])

        # resolve quando o 's no final de uma palavra não é separado em outro token
        if len(named_entity) > 2 and named_entity.endswith("'s"):
            named_entity = named_entity[:-2]

        return named_entity

    def is_first_word_and_not_np(self, i, word):
        tag = word[1]
        if i == 0 and not tag == 'NN' and not tag == 'NNP':
            return True
        return False

    def is_complement(self, word):
        text = word[0]
        return text in ("of", "the", "'s")

    def is_first_letter_upper(self, word):
        text = word[0]
        return text[0].isupper()

    def has_np(self, ne):
        for word in ne:
            tag = word[1]
            if tag == 'NN' or tag == 'NNP':
                return True
        return False

    def create_ne_file(self):
        # para nao repetir os elementos
        self.named_entities = set(self.named_entities)
        self.named_entities = list(self.named_entities)
        self.named_entities.sort()
        with open("entidades_nomeadas.csv", 'w', encoding="utf-8") as article_file:
            for entidade in self.named_entities:
                article_file.write("{0}\n".format(entidade))

    def remove_unfinished_complements(self, ne):
        if self.is_complement(ne[-1]):
            return ne[:-1]
        else:
            return ne

    def read_test_file(self):
        with open("tests/ne_baelor_s1e9.csv", 'r') as test_file:
            test = test_file.readlines()
            ne_test = []
            for ne in test:
                ne_test.append(ne)
            ne_test.sort()
        with open("tests/ne_baelor_s1e9_ordenado.csv", 'w') as test_file_write:
            for ne in ne_test:
                test_file_write.write(ne)


# extractor = NEExtractor("second_processing/Baelor s1e9_tests.txt")

seasons_files = glob.glob("pre_processed_documents/*")
for season in seasons_files:
    season_name = os.path.basename(season)

    episodes_files = glob.glob(season + "/*.txt")
    for episode in episodes_files:
        extractor = NEExtractor(episode)
        # print(episode)
    extractor.create_ne_file()

# primeira tentativa de extrair entidades nomeadas no arquivo Baelor.txt
# 873 entidades nomeadas

# segunda tentativa: transformando de lista pra conjunto
# 319 entidades nomeadas

# terceira tentativa: colocando ne seguidas como uma só
# 336 entidades nomeadas
# muitas substrings repetidas

# quarta tentativa: mudando o pre-processamento
# apenas com as secoes: Plot, Summary, Appearances and Deaths
# 113 endidades nomeadas

# quinta tentativa: consertando o metodo que junta mais de uma NE seguidas
# 105 entidades nomeadas

# sexta tentativa: migrando o codigo do java pro python
# 103 entidades nomeadas