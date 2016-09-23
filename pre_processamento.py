import re


class ArticleReader:
    title = None
    texto = None
    conteudo = []

    def __init__(self, from_path):
        with open(from_path, 'r') as f:
            text_lines = f.readlines()
            text_file = " ".join(text_lines)
            self.extrai_titulo(text_file)
            self.corta_edit(text_lines)
            self.corta_image_galerry()

    def extrai_titulo(self, texto):
        regex_1 = re.compile(r'"(.+)"')
        list = re.findall(regex_1, texto)
        self.title = list[0]

    def corta_image_galerry(self):
        regex_2 = re.compile(r'(".*)Ima', flags=re.DOTALL)
        list_2 = re.findall(regex_2, self.texto)
        self.texto = list_2[0]

    def corta_edit(self, text_file):
        for line in text_file:
            regex_3 = re.compile(r'^.*Edit')
            regex_4 = re.compile(r'(^.*)Edit')
            list_1 = re.findall(regex_3, line)
            list_2 = re.findall(regex_4, line)

            if list_1:
                line = re.sub(regex_3, list_2[0], line)
            if line != '\n':
                self.conteudo.append(line)
        self.texto = " ".join(self.conteudo)

    def save_articles(self, to):
        with open(to + "/" + self.title + ".txt", 'w') as article_file:
            article_file.write(self.texto)


article = ArticleReader("raw_documents/season_1/a_golden_crown.txt")
article.save_articles("documents")
