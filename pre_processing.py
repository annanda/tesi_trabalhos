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

    def extrai_titulo(self, texto):
        regex_1 = re.compile(r'"(.+)"')
        list = re.findall(regex_1, texto)
        self.title = list[0]
        regex_season = re.compile(r'Season ([1-9]+)')
        season_number = re.findall(regex_season, texto)
        season_number = season_number[0]
        regex_episode = re.compile(r'Episode ([1-9]+)')
        episode_number = re.findall(regex_episode, texto)
        episode_number = episode_number[0]

        self.title = self.title + " s" + season_number + "e" + episode_number

    # def save_articles(self, to):
    #     with open(to + "/" + self.title + ".txt", 'w') as article_file:
    #         article_file.write(self.texto_final)

# all_seasons_files = []
#
# for season in glob.glob("raw_documents/*"):
#     all_seasons_files.append(season)

# for season in all_seasons_files:
#     file_list = glob.glob(season + "/*.txt")
#     # print(file_list)
#     regex = re.compile(r'raw_documents\/(season_[1-6])')
#     season_number = re.findall(regex, season)
#     for episode in file_list:
#         article = ArticleReader(episode)
#         article.save_articles("documents/" + season_number[0])

article = ArticleReader("documents/season_1/Baelor.txt")
print(article.title)