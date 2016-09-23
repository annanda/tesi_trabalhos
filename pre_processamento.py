import re


class ArticleReader:
    title = None
    conteudo = []

    def __init__(self, from_path):
        with open(from_path, 'r') as f:
            text_file = f.read()
            self.extrai_titulo(text_file)
            self.corta_image_galerry(text_file)
            self.corta_edit()


    def extrai_titulo(self, texto):
        regex_1 = re.compile(r'"(.+)"')
        list = re.findall(regex_1, texto)
        self.title = list[0]

    def corta_image_galerry(self, texto):
        regex_2 = re.compile(r'(".*)Ima', flags=re.DOTALL)
        list_2 = re.findall(regex_2, texto)
        self.conteudo = list_2[0]

    def corta_edit(self):
        regex_3 = re.compile(r'^.*Edit', flags=re.MULTILINE)
        regex_4 = re.compile(r'(^.*)Edit', flags=re.MULTILINE)
        lista_1 = re.sub(r'^.*Edit', r'(^.*)Edit', self.conteudo)
        self.conteudo = lista_1
        print(self.conteudo)
        # lista_2 = re.findall(regex_4, self.conteudo)
        # for palavras in lista_1:


    def save_articles(self, to):
        with open(to + "/" + self.title + ".txt", 'w') as article_file:
            article_file.write(self.conteudo)



article = ArticleReader("raw_documents/season_1/a_golden_crown.txt")
# article.save_articles("documents")
# print(article.conteudo)
# print(article.title)
# print(len(article.conteudo))
