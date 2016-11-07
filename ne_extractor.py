import jsonpickle
from ne import EN
import nltk
import glob
import os.path


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
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

    return tagged_sentences


def get_ne(tagged_sentences):
    named_entities = []

    ne = []
    for i, sentence in enumerate(tagged_sentences):
        start_index = None
        for j, tagged_word in enumerate(sentence):

            if j == 0:
                continue

            if is_first_letter_upper(tagged_word):
                ne.append(tagged_word)

                if start_index is None:
                    start_index = j

                if j != len(sentence) - 1:
                    continue

            if ne and is_complement(tagged_word):
                ne.append(tagged_word)
                if j != len(sentence) - 1:
                    continue

            if ne:
                if has_np(ne):
                    ne = remove_unfinished_complements(ne)
                    named_entity = sentence_text(ne)

                    # resolve quando o 's no final de uma palavra não é separado em outro token
                    if len(named_entity) > 2 and named_entity.endswith("'s"):
                        named_entity = named_entity[:-2]

                    if len(named_entity) > 2:  # remove entidades com apenas duas letras
                        en = EN(named_entity)
                        en.start_index = start_index
                        en.sentence = sentence_without_tag(sentence)
                        named_entities.append(en)

                start_index = None
                ne.clear()

    return named_entities


def sentence_text(sentence):
    return " ".join([word[0] for word in sentence])


def sentence_without_tag(sentence):
    return [word[0] for word in sentence]


def is_complement(word):
    text = word[0]
    return text in ("of", "the", "'s")


def is_first_letter_upper(word):
    text = word[0]
    return text[0].isupper()


def has_np(ne):
    for word in ne:
        tag = word[1]
        if tag == 'NN' or tag == 'NNP':
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
    for season_dir in seasons_dirs:
        # season_name = os.path.basename(season_dir)

        episodes_files = glob.glob(season_dir + "/*.txt")
        for episode_file in episodes_files:
            extracted_nes = extract_nes(episode_file)
            nes.extend(extracted_nes)

    return nes


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


if __name__ == "__main__":
    entities = extract_nes_from_episodes()
    create_ne_csv(entities)
    create_ne_json(entities)
    create_ne_with_sentence_csv(entities)

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
