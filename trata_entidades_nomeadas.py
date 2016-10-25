with open("entidades_nomeadas.csv", 'r') as test_file:
    entidades_nomeadas = test_file.readlines()
    novas_entidades_nomeadas =[]
    for i, ne in enumerate(entidades_nomeadas):
        ne_dividida = ne.split()
        if ne_dividida[0] in ["Lady"]:
            if len(ne_dividida) > 1:
                if ne_dividida[1] not in ["of"]:
                    print(ne_dividida[1:])
                    ne_nova = " ".join(ne_dividida[1:])
                    # print(ne_nova)
                    novas_entidades_nomeadas.append(ne_nova + "\n")
                else:
                    novas_entidades_nomeadas.append(ne)
        else:
            novas_entidades_nomeadas.append(ne)
print(novas_entidades_nomeadas)
en = set(novas_entidades_nomeadas)
en_2 = list(en)
novas_entidades_nomeadas = set(novas_entidades_nomeadas)
# print(len(novas_entidades_nomeadas))
with open("novas_entidades_nomeadas", 'w') as test_file_write:
    for ne in en_2:
        test_file_write.write("{0}".format(ne))
print(len(en_2))


# primeira tentativa de melhorar entidades nomeadas:
# tira os Lady
# 1284 entidades nomeadas (estava 1295)