# Trabalhos da disciplina Tópicos Especiais em Sistemas Inteligentes II (TESI II) de Ciência da Computação da UFRJ

## Requisitos
Esse projeto foi feito para funcionar usando **Python 3**. Para rodar, é preciso instalar os requisitos presentes no arquivo ```requirements.txt```.

Recomenda-se o uso do ```pip```  e ```virtualenv``` para baixar as dependencias e mante-las isoladas.

## Pastas

- final_results

  Arquivos que representam os resultados finais do trabalho. Foram entregues para o professor.

- experiments

  Arquivos gerados ao longo do trabalho para ajudar na analise e criação das regras. Contém, por exemplo, listas de entidades nomeadas marcadas manualmente

- generated

  Pasta usada para guardar os arquivos gerados pelos programas. É ignorada pelo git, evitando assim que o repositorio contenha os arquivos que foram gerados automaticamente.

- raw_documents

  Contem os textos de Game of Thrones que foram usados como base para o trabalho.

- src

  Contêm os arquivos python que fazem as análises nos textos.

## Como usar

Ao contrário do ```tf-idf.py```, todos os arquivos só precisam ser rodados normalmente para gerar seus resultados. Só é importante que eles sejam rodados na ordem certa, pois o resultado de um depende de um arquivo gerado pelo anterior.
No caso do ```tf-idf```, é possível realizar buscas através da linha de comando.

### Ordem

A ordem correta para executar os arquivo é:

- ```pre_processamento.py```

  faz o pre-processamento do texto deixando apenas o que nos interessa: as informações sobre a história em cada episódio da série.

- ```ne_extractor.py```

  faz a extração inicial de entidades nomeadas de todos os arquivos de episódios da série.

- ```classifica_e_reune.py```

  melhora o conjunto de entidades nomeadas. Olhando quais entidades se referem ao mesmo elemento e elimina as repetições. Além disso, também classifica as entidades.

- ```extract_relations.py```

  faz a extração das relações entre entidades

### TF-IDF

O ```tf-idf.py``` pode ser usado pela linha de comando para realizar buscas nos documentos. Para funcionar, é importante que o ```pre-processamento.py``` já tenha sido executado.
Ex:

```tf-idf.py "Eddar Stark"```

Esse comando irá buscar documentos relevantes para Eddar Stark e mostrar no terminal os documentos por relevancia, de forma descendente.