import re
import glob


class ArticleReader:

    def __init__(self, from_path):
        self.title = None
        self.texto = None
        self.texto_final = None
        self.conteudo = []
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
        list_2 = re.findall(regex_2, self.texto_final)
        if list_2:
            self.texto_final = list_2[0]

    def corta_edit(self, text_lines):
        for line in text_lines:
            regex_3 = re.compile(r'^.*Edit')
            regex_4 = re.compile(r'(^.*)Edit')
            list_1 = re.findall(regex_3, line)
            list_2 = re.findall(regex_4, line)

            if list_1:
                line = re.sub(regex_3, list_2[0], line)
            if line != '\n':
                self.conteudo.append(line)
        self.texto_final = " ".join(self.conteudo)

    def save_articles(self, to):
        with open(to + "/" + self.title + ".txt", 'w') as article_file:
            article_file.write(self.texto_final)

all_seasons_files = []

for season in glob.glob("raw_documents/*"):
    all_seasons_files.append(season)

for season in all_seasons_files:
    file_list = glob.glob(season + "/*.txt")
    # print(file_list)
    regex = re.compile(r'raw_documents\/(season_[1-6])')
    season_number = re.findall(regex, season)
    for episode in file_list:
        article = ArticleReader(episode)
        article.save_articles("documents/" + season_number[0])
