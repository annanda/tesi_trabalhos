import re
from fuzzywuzzy import fuzz, process

with open("entidades_nomeadas.csv", 'r') as test_file:
    entidades_nomeadas = test_file.readlines()
    novas_entidades_nomeadas = []
    for i, ne in enumerate(entidades_nomeadas):
        ne_dividida = ne.split()
        if ne_dividida[0] in ["Lady", "Prince", "Ser", "Lord", "Lords"]:
            if len(ne_dividida) > 1:
                if ne_dividida[1] not in ["of", "'s"]:
                    # print(ne_dividida[1:])
                    ne_nova = " ".join(ne_dividida[1:])
                    # print(ne_nova)
                    novas_entidades_nomeadas.append(ne_nova + "\n")
                else:
                    novas_entidades_nomeadas.append(ne)
        else:
            novas_entidades_nomeadas.append(ne)
# print(novas_entidades_nomeadas)
en = set(novas_entidades_nomeadas)
en_2 = list(en)
en_2.sort()
# print(len(novas_entidades_nomeadas))
with open("novas_entidades_nomeadas.csv", 'w') as test_file_write:
    for ne in en_2:
        test_file_write.write("{0}".format(ne))
# print(len(en_2))



with open("novas_entidades_nomeadas.csv", 'r') as test_file:
    entidades_nomeadas = test_file.readlines()
    entidades_um_nome = []
    entidades_mais_nome = []

    for ne in entidades_nomeadas:
        ne_dividida = ne.split()
        if len(ne_dividida) > 1:
            entidades_mais_nome.append(ne.replace("\n", ""))
        elif len(ne_dividida) == 1:
            entidades_um_nome.append(ne.replace("\n", ""))
entidades_relacionadas = {}

with open("entidades_nomeadas_relacionadas", 'w') as test_file:
    for um_nome in entidades_um_nome:
        entidades_relacionadas[um_nome] = process.extract(um_nome, entidades_mais_nome, scorer=fuzz.partial_ratio, limit=4)
        test_file.write("Entidade: " + um_nome + "\n")
        test_file.write("Relacionadas " + str(entidades_relacionadas[um_nome]) + "\n\n")



# primeira tentativa de melhorar entidades nomeadas:
# tira os Lady
# 1284 entidades nomeadas (estava 1295)

# segunda tentatica
# tira os Prince
# 1274 entidades nomeadas (estava 1284)

# tirando as entidades nomeadas com tamanho menor que 3 caracteres
# 1286 entidades nomeadas


# terceira tentativa
# depois de mudar o pre-processamento substituindo os caracteres ruins
# tirando o Lady e Prince
# 1265 entidades nomeadas (era 1274)

# quarta tentativa
# tirando o Ser da frente dos nomes
# 1233 entidades nomeadas (era 1265)

# quinta tentativa
# Tira Lord da frente dos nomes
# 1199 entidades
# adiciona o 's na lista dos segundos a se ignorar

# sexta tentativa
# Tira Lords da frente dos nomes
# 1197 entidades

# setima tentativa
# usa o ne_extractor ignorando sempre a primeira palavra da sentenca
# 1138 entidades

# Tentativa de usar a lib fuzzywuzzy que usa algoritmos fuzzy para comparar strings
# usei o metodo process.extract com fuzz.partial_ratio para obter substrings de uma string
# Peguei coisas boas, mas muito mais coisas não boas
# BOA-->
# Entidade:  Aegon
# Relacionadas  [('Aegon I Targaryen', 80), ('Aegon Targaryen', 80), ('Aegon the Conquer', 80), ('Aegon the Conqueror', 80)]
# RUIM -->
# Entidade:  Aggo
# Relacionadas  [('Aegon I Targaryen', 50), ('Aegon Targaryen', 50), ('Aegon the Conquer', 50), ('Aegon the Conqueror', 50)]
