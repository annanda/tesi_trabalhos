class EN:
    def __init__(self):
        self._original = None
        self.owords = []
        self._canonico = None
        self.cwords = []
        self.classification = None

    @property
    def canonico(self):
        return self._canonico

    @canonico.setter
    def canonico(self, value):
        self._canonico = value

        if value is not None:
            self.cwords = value.split(" ")
        else:
            self.cwords = []

    @property
    def original(self):
        return self._original

    @original.setter
    def original(self, value):
        self._original = value

        if value is not None:
            self.owords = value.split(" ")
        else:
            self.owords = []

    def __str__(self):
        return "{0} ({1}) - {2}".format(self.canonico, self.original, self.classification)


with open("entidades_nomeadas.csv", 'r') as file:
    lines = file.readlines()
    lines = map(lambda l: l.strip(), lines)

entidades = []
for line in lines:
    entidade = EN()
    entidade.original = line
    entidade.canonico = entidade.original
    entidade.classification = "other"
    entidades.append(entidade)

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

with open("classifica_e_reune10.csv", 'w+') as file:
    for entidade in entidades:
        file.write(str(entidade))
        file.write("\n")

for entidade in entidades:
    print(entidade)
print("\n----------------\n")
quantas_entidades = len(entidades)
quantas_entidades_pos_processamento = len(set([en.canonico for en in entidades]))
quantas_entidades_com_other = len([en for en in entidades if en.classification == "other"])
quantas_entidades_com_person = len([en for en in entidades if en.classification == "person"])

print("De {0} entidades para {1} entidades.".format(quantas_entidades, quantas_entidades_pos_processamento))
print("Entidades com other: {0} ({1})".format(quantas_entidades_com_other,
                                              quantas_entidades_com_other / quantas_entidades * 100))
print("Entidades com person: {0} ({1})".format(quantas_entidades_com_person,
                                               quantas_entidades_com_person / quantas_entidades * 100))

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

# O que fazer com ens que são "Lady", "Lord Commander", "Lord 's Choosen", etc...

# Palavra The:
# Nada. Aparentemente, tudo que começa com The não se refere a mais nada

# Palavra "Houses"
