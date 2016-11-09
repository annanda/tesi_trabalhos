from collections import Counter

import jsonpickle
from ne import EN
import nltk
import glob
import re


def extract_nes(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        text = file.read()

    return get_ne(tag_sentences(text))


def tag_sentences(text):
    lines = text.split("\n")

    sentences = []
    for line in lines:
        tokenized_lines = nltk.sent_tokenize(line)
        for tokenized_line in tokenized_lines:
            sentences += re.split(r'[^\.]\.\s', tokenized_line)

    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

    for s in tokenized_sentences:
        every_token.extend(s)

    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

    return tagged_sentences


def get_ne(tagged_sentences):
    named_entities = []
    tokens = []

    for i, sentence in enumerate(tagged_sentences):
        start_index = None
        in_doubt = False
        for j, tagged_word in enumerate(sentence):

            if is_first_letter_upper(tagged_word):
                tokens.append(tagged_word)

                if j == 0 or sentence[j - 1] in ["''", "``", "'"]:
                    in_doubt = True

                if start_index is None:
                    start_index = j

                if j != len(sentence) - 1:
                    continue

            if tokens and is_complement(tagged_word):
                tokens.append(tagged_word)
                if j != len(sentence) - 1:
                    continue

            if tokens:
                if has_noun_tag(tokens):
                    tokens = remove_unfinished_complements(tokens)
                    entity_name = sentence_text(tokens)

                    # resolve quando o 's no final de uma palavra não é separado em outro term
                    if len(entity_name) > 2 and entity_name.endswith("'s"):
                        entity_name = entity_name[:-2]

                    if len(entity_name) > 2:  # remove entidades com apenas duas letras
                        en = EN(entity_name)
                        en.start_index = start_index
                        en.sentence = sentence_without_tag(sentence)
                        en.in_doubt = in_doubt

                        named_entities.append(en)

                in_doubt = False
                start_index = None
                tokens.clear()

    return named_entities


def sentence_text(sentence):
    return " ".join([word[0] for word in sentence])


def sentence_without_tag(sentence):
    return [word[0] for word in sentence]


def is_complement(word):
    text = word[0]
    return text in ("of", "the", "'s", "'")


def is_first_letter_upper(word):
    text = word[0]
    return text[0].isupper()


def has_noun_tag(ne):
    for word in ne:
        tag = word[1]
        if tag in ['NN', 'NNP', 'NNS', 'NNPS']:
            return True
    return False


def remove_unfinished_complements(ne):
    ne_without_trailing_complements = list(ne)
    for i in range(len(ne) - 1, 0, -1):
        if is_complement(ne[i]):
            ne_without_trailing_complements = ne_without_trailing_complements[:-1]
        else:
            break
    return ne_without_trailing_complements


def extract_nes_from_episodes():
    nes = []

    seasons_dirs = glob.glob("pre_processed_documents/*")

    if len(seasons_dirs) == 0:
        print("Nenhum episodio achado...")
        exit(-1)

    for season_dir in seasons_dirs:
        episodes_files = glob.glob(season_dir + "/*.txt")
        for episode_file in episodes_files:
            extracted_nes = extract_nes(episode_file)
            nes.extend(extracted_nes)

    frequency_counter = Counter(every_token)
    verified_nes = []
    for ne in nes:
        if ne.in_doubt:
            first_word = ne.owords[0]
            freq = frequency_counter[first_word]
            freq_lower = frequency_counter[first_word.lower()]
            if (freq > 1 and freq_lower == 0) or is_name_start(first_word):
                verified_nes.append(ne)
        else:
            verified_nes.append(ne)

    return verified_nes


def is_name_start(word):
    return word in "The Ser Prince Princess King Queen Lady Commander Lord Grand Septa Khal Maester".split()


def create_ne_csv(named_entities):
    named_entities = map(lambda ne: ne.original, named_entities)

    # para nao repetir os elementos
    named_entities = set(named_entities)
    named_entities = list(named_entities)
    named_entities.sort()
    with open("entidades_nomeadas.csv", 'w', encoding="utf-8") as file:
        for entidade in named_entities:
            file.write("{0}\n".format(entidade))


def create_ne_with_sentence_csv(named_entities):
    named_entities = [(ne.original, " ".join(ne.sentence)) for ne in named_entities]

    named_entities = sorted(list(set(named_entities)))
    with open("entidades_nomeadas_with_sentence.csv", 'w', encoding="utf-8") as file:
        for entidade in named_entities:
            file.write("{0},{1}\n".format(entidade[0], entidade[1]))


def create_ne_json(named_entities):
    with open("entidades_nomeadas.json", 'w', encoding="utf-8") as file:
        file.write(jsonpickle.encode(named_entities))


every_token = []

if __name__ == "__main__":
    entities = extract_nes_from_episodes()

    create_ne_csv(entities)
    create_ne_json(entities)
    create_ne_with_sentence_csv(entities)

# primeira tentativa de extrair entidades nomeadas no arquivo Baelor.txt
# 873 entidades nomeadas

# segunda tentativa: transformando de lista pra conjunto no arquivo Baelor.txt
# 319 entidades nomeadas

# terceira tentativa: colocando ne seguidas como uma só no arquivo Baelor.txt
# 336 entidades nomeadas
# muitas substrings repetidas

# quarta tentativa: mudando o pre-processamento
# apenas com as secoes: Plot, Summary, Appearances and Deaths
# 113 endidades nomeadas

# quinta tentativa: consertando o metodo que junta mais de uma NE seguidas
# 105 entidades nomeadas

# sexta tentativa: migrando o codigo do java pro python
# 103 entidades nomeadas

# tentativa anterior, usando Java
# 2778 entidades nomeadas

# juntanto todos os documentos
# 1296 entidades nomeadas

# eliminando entidades nomeadas de tamanho menor que 1
# 1295 entidades nomeadas

# ignorando sempre a primeira palavra de cada sentenca
# 1227 entidades nomeadas

# Levando em consideração a primeira palavra, mas só considerando ela se não aparecer em outra parte do texto
# Aceitando NNS e NNPS
# 1273 entidades nomeadas
