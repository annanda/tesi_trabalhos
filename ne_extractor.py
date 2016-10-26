import nltk
import re
import glob
import os.path
from collections import Counter


class NEExtractor:
    named_entities = []

    info_about_named_entities = []

    def __init__(self, article_path):

        with open(article_path, 'r', encoding="utf-8") as article:
            self.article = article.read()

        self.get_ne(self.nominated_entities())

    def nominated_entities(self):
        lines = self.article.split("\n")

        sentences = []
        for line in lines:
            sentences += nltk.sent_tokenize(line)

        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

        return tagged_sentences

    def get_ne(self, tagged_sentences):
        ne = []
        for i, sentence in enumerate(tagged_sentences):
            for j, tagged_word in enumerate(sentence):

                if j == 0:
                    continue

                if self.is_first_letter_upper(tagged_word):
                    ne.append(tagged_word)
                    if j != len(sentence) - 1:
                        continue

                if ne and self.is_complement(tagged_word):
                    ne.append(tagged_word)
                    if j != len(sentence) - 1:
                        continue

                if ne:
                    if self.has_np(ne):
                        ne = self.remove_unfinished_complements(ne)
                        named_entity = self.sentence_text(ne)

                        # resolve quando o 's no final de uma palavra não é separado em outro token
                        if len(named_entity) > 2 and named_entity.endswith("'s"):
                            named_entity = named_entity[:-2]

                        if len(named_entity) > 2:
                            # self.info_about_named_entities.append([self.sentence_text_with_tags(ne), self.sentence_text_with_tags(sentence), self.sentence_text(sentence)])
                            self.named_entities.append(named_entity)

                    ne.clear()

    def sentence_text_with_tags(self, sentence):
        result = []
        for word in sentence:
            result.append(word[0] + "_" + word[1])

        return " ".join(result)

    def sentence_text(self, sentence):
        return " ".join([word[0] for word in sentence])

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

    def remove_unfinished_complements(self, ne):
        ne_without_trailing_complements = list(ne)
        for i in range(len(ne)-1, 0, -1):
            if self.is_complement(ne[i]):
                ne_without_trailing_complements = ne_without_trailing_complements[:-1]
            else:
                break
        return ne_without_trailing_complements

    def create_ne_file(self):

        # counter = Counter(self.named_entities)
        # for i, named_entity in enumerate(self.named_entities):
        #     freq = counter[named_entity]
        #     self.info_about_named_entities[i] = [named_entity, str(freq)] + self.info_about_named_entities[i]
        #
        # for info in self.info_about_named_entities:
        #     str_info = []
        #     for data in info:
        #         str_info += ['"' + data + '"']
        #     print(",".join(str_info))

        # para nao repetir os elementos
        self.named_entities = set(self.named_entities)
        self.named_entities = list(self.named_entities)
        self.named_entities.sort()
        with open("entidades_nomeadas.csv", 'w', encoding="utf-8") as article_file:
            for entidade in self.named_entities:
                article_file.write("{0}\n".format(entidade))


# extractor = NEExtractor("pre_processed_documents/season_4/breaker_of_chains.txt")

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

# juntanto todos os documentos
# 1296 entidades nomeadas

# eliminando entidades nomeadas de tamanho menor que 1
# 1295 entidades nomeadas

# ignorando sempre a primeira palavra de cada sentenca
# 1227 entidades nomeadas
