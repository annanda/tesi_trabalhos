from collections import defaultdict

import jsonpickle
from ne import EN


# with open("entidades_nomeadas.csv", 'r') as file:
#     lines = file.readlines()
#     lines = map(lambda l: l.strip(), lines)
#
# entidades = []
# for line in lines:
#     entidade = EN()
#     entidade.original = line
#     entidade.canonico = entidade.original
#     entidade.classification = "other"
#     entidades.append(entidade)


class Ocurrence:
    def __init__(self, index, sentence):
        self.index = index
        self.sentence = sentence


with open("entidades_nomeadas.json", 'r') as file:
    entidades = jsonpickle.decode(file.read())

ne_ocurrences = {}
for entidade in entidades:
    if entidade.original not in ne_ocurrences:
        ne_ocurrences[entidade.original] = []
    ne_ocurrences[entidade.original].append(Ocurrence(entidade.start_index, entidade.sentence))

entidades = sorted(list(set(entidades)))

for entidade in entidades:

    if entidade.owords[0] == "Ser":
        entidade.canonico = " ".join(entidade.owords[1:])
        entidade.classification = "person"

    if len(entidade.owords) > 1 and entidade.owords[0] == "Prince" and entidade.owords[1] != "of":
        entidade.canonico = " ".join(entidade.owords[1:])
        entidade.classification = "person"

    if len(entidade.owords) > 1 and entidade.owords[0] == "Princess" and entidade.owords[1] != "of":
        entidade.canonico = " ".join(entidade.owords[1:])
        entidade.classification = "person"

    if len(entidade.owords) > 1 and entidade.owords[0] == "King" and entidade.owords[1] not in ["of", "'s"]:
        entidade.canonico = " ".join(entidade.owords[1:])
        entidade.classification = "person"

    if len(entidade.owords) > 1 and entidade.owords[0] == "Queen" and entidade.owords[1] not in ["of", "Regent"]:
        entidade.canonico = " ".join(entidade.owords[1:])
        entidade.classification = "person"

    if len(entidade.owords) > 1 and entidade.owords[0] == "Lady" and entidade.owords[1] != "of":
        entidade.canonico = " ".join(entidade.owords[1:])
        entidade.classification = "person"

    if len(entidade.owords) > 1 and entidade.owords[0] == "Commander" and entidade.owords[1] != "of":
        entidade.canonico = " ".join(entidade.owords[1:])
        entidade.classification = "person"

    if len(entidade.owords) > 2 \
            and entidade.owords[0] == "Lord" \
            and entidade.owords[1] == "Commander" \
            and entidade.owords[2] != "of":
        entidade.canonico = " ".join(entidade.owords[2:])
        entidade.classification = "person"

    if len(entidade.owords) > 2 \
            and entidade.owords[0] == "Queen" \
            and entidade.owords[1] == "Regent" \
            and entidade.owords[2] != "of":
        entidade.canonico = " ".join(entidade.owords[2:])
        entidade.classification = "person"

    if len(entidade.owords) > 1 \
            and entidade.owords[0] == "Lord" \
            and entidade.owords[1] != "of" \
            and entidade.owords[1] != "Commander":  # evita pegar os "Lord Commander", que já foram tratados
        entidade.canonico = " ".join(entidade.owords[1:])
        entidade.classification = "person"

house_names = []
for entidade in entidades:

    if len(entidade.owords) >= 2 and entidade.owords[0] == "House" and entidade.owords[1] != "of":
        entidade.classification = "house"

        house_names.append(entidade.owords[1])

names_to_full_names = {}
for entidade in entidades:

    if entidade.classification != "house" and len(entidade.cwords) == 2 and entidade.cwords[1] in house_names:
        entidade.classification = "person"
        names_to_full_names[entidade.cwords[0]] = entidade.canonico

for entidade in entidades:

    if len(entidade.cwords) == 1 and entidade.cwords[0] in names_to_full_names.keys():
        entidade.classification = "person"
        entidade.canonico = names_to_full_names[entidade.cwords[0]]

for entidade in entidades:

    if entidade.classification == "other":
        sounds_like_a_place = 0
        for ocurrence in ne_ocurrences[entidade.original]:
            if ocurrence.index > 2 \
                    and ocurrence.sentence[ocurrence.index - 3] == "return" \
                    and ocurrence.sentence[ocurrence.index - 2] == "home" \
                    and ocurrence.sentence[ocurrence.index - 1] == "to":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "in" \
                    and ocurrence.sentence[ocurrence.index - 1] == "the":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "visit" \
                    and ocurrence.sentence[ocurrence.index - 1] == "to":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "return" \
                    and ocurrence.sentence[ocurrence.index - 1] == "to":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "out" \
                    and ocurrence.sentence[ocurrence.index - 1] == "of":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "back" \
                    and ocurrence.sentence[ocurrence.index - 1] == "to":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "at" \
                    and ocurrence.sentence[ocurrence.index - 1] == "the":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "return" \
                    and ocurrence.sentence[ocurrence.index - 1] == "from":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "arrive" \
                    and ocurrence.sentence[ocurrence.index - 1] == "at":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "from" \
                    and ocurrence.sentence[ocurrence.index - 1] == "the":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "leave" \
                    and ocurrence.sentence[ocurrence.index - 1] == "for":
                sounds_like_a_place += 1
            elif ocurrence.index > 1 \
                    and ocurrence.sentence[ocurrence.index - 2] == "to" \
                    and ocurrence.sentence[ocurrence.index - 1] == "the":
                sounds_like_a_place += 1
            elif ocurrence.index > 0 and ocurrence.sentence[ocurrence.index - 1] in ["at", "in", "depart", "on", "to", "near", "reaches", "outside", "from"]:
                sounds_like_a_place += 1

        if sounds_like_a_place > 0:
            print("{0} {1}/{2} ({3}%)".format(entidade, sounds_like_a_place, len(ne_ocurrences[entidade.original]), sounds_like_a_place/len(ne_ocurrences[entidade.original])*100))

        if sounds_like_a_place > 5:
            entidade.classification = "place"

with open("classifica_e_reune11.csv", 'w+') as file:
    for entidade in entidades:
        file.write(str(entidade))
        file.write("\n")

# with open("classifica_e_reune.json", 'w+') as file:
#     file.write(jsonpickle.encode(entidades))

# for entidade in entidades:
#     print(entidade)

print("\n----------------\n")

quantas_entidades = len(entidades)
quantas_entidades_pos_processamento = len(set([en.canonico for en in entidades]))
quantas_entidades_com_other = len([en for en in entidades if en.classification == "other"])
quantas_entidades_com_person = len([en for en in entidades if en.classification == "person"])
quantas_entidades_com_place = len([en for en in entidades if en.classification == "place"])

print("De {0} entidades para {1} entidades.".format(quantas_entidades, quantas_entidades_pos_processamento))
print("Entidades com other: {0} ({1})".format(quantas_entidades_com_other,
                                              quantas_entidades_com_other / quantas_entidades * 100))
print("Entidades com person: {0} ({1})".format(quantas_entidades_com_person,
                                               quantas_entidades_com_person / quantas_entidades * 100))
print("Entidades com place: {0} ({1})".format(quantas_entidades_com_place,
                                              quantas_entidades_com_place / quantas_entidades * 100))

# Titulos:
# Remover os titulos do nome canonico
# Lord [DONE]
# Commander [DONE]
# Lord Commander [DONE]
# Prince [DONE]
# Princess [DONE]
# Lady [DONE]
# Ser [DONE]
# King [DONE]
# Queen [DONE]
# Queen Regent [DONE]
# Meister
# Grand Meister

# Tirar ' no final do nomes

# Substituit '' e `` por "

# O que fazer com ens que são "Lady", "Lord Commander", "Lord 's Choosen", etc...

# Palavra The:
# Nada. Aparentemente, tudo que começa com The não se refere a mais nada

# Prefixos de lugares
# at
# depart
# in
# out of
# in the
# at the
# back to

# Palavra "Houses"
