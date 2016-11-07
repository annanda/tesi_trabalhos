import jsonpickle
import nltk


class Sentence:
    def __init__(self, tokens, entities):
        self.tokens = tokens
        self.entities = entities


def create_relations_csv(all_relations):
    with open("extract_relations.csv", "w+", encoding="utf-8") as file:
        for relation in all_relations:
            file.write("{0}, {1}, {2}\n".format(relation[0], relation[1], relation[2]))


def create_relation_names_csv(all_relations):
    all_relation_names = [relation[1] for relation in all_relations]
    all_relation_names = set(all_relation_names)
    with open("extract_relations_names.csv", "w+", encoding="utf-8") as file:
        for name in all_relation_names:
            file.write("{0}\n".format(name))


def group_entities_by_sentence(entities):
    entities_by_sentence = {}
    for entity in entities:
        sentence = " ".join(entity.sentence)
        if sentence not in entities_by_sentence:
            entities_by_sentence[sentence] = []

        entities_by_sentence[sentence].append(entity)

    sentences = []
    for sentence_text in entities_by_sentence:
        tokenized_sentence = entities_by_sentence[sentence_text][0].sentence
        tagged_sentence = nltk.pos_tag(tokenized_sentence)

        entities = entities_by_sentence[sentence_text]
        sorted_entities = sorted(entities, key=lambda e: e.start_index)

        sentence = Sentence(tagged_sentence, sorted_entities)
        sentences.append(sentence)

    return sentences


def extract_relations(sentence):
    relations = []
    entities = sentence.entities
    for (entity1, entity2) in zip(entities, entities[1:]):
        start_index = entity1.start_index + len(entity1.original)
        end_index = entity2.start_index - 1
        for i in range(start_index, end_index):
            if sentence.tokens[i][1] in ["VB", "VBG", "VBZ", "VBN"]:
                relation = (entity1.canonico, sentence.tokens[i][0], entity2.canonico)
                relations.append(relation)
                print(str(relation), " ".join([token[0]+" "+token[1] for token in sentence.tokens]))

    return relations


def main():
    with open("entidades_nomeadas.json", "r", encoding="utf-8") as file:
        entities = jsonpickle.decode(file.read())

    sentences = group_entities_by_sentence(entities)

    all_relations = []
    for sentence in sentences:
        relations = extract_relations(sentence)

        all_relations.extend(relations)

    create_relations_csv(all_relations)
    create_relation_names_csv(all_relations)


if __name__ == "__main__":
    main()

# usar o reunido e classificado para gerar resultados mais bonitos
# usar as classes para impedir relações (Ex. Lugar não faz nada com pessoa).
# entender melhor as tags que começam com "VB" e saber se faz sentido reunir em uma palavra, espandir, etc...