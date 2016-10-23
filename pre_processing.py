import re
import glob


class ArticleReader:

    def __init__(self, from_path):
        self.title = None
        self.plot = None
        self.summary = None
        self.appearences = None
        self.deaths = None
        self.quotes = None
        self.texto_final = None
        with open(from_path, 'r') as f:
            text_lines = f.readlines()
            text_file = " ".join(text_lines)
            self.extrai_titulo(text_file)
            self.get_plot(text_file)
            self.get_summary(text_file)
            self.get_appearences(text_file)
            self.get_deaths(text_file)
            self.get_quote(text_file)
            self.monta_texto_final()
            self.save_articles("second_processing")

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

    def get_plot(self, texto):
        regex_1 = re.compile(r'Plot(.*)Summary', flags=re.DOTALL)
        list = re.findall(regex_1, texto)
        self.plot = list[0]

    def get_summary(self, texto):
        regex_1 = re.compile(r'Summary(.*)Appearances\n\s Main', flags=re.DOTALL)
        list = re.findall(regex_1, texto)
        self.summary = list[0]

    def get_appearences(self, texto):
        regex_1 = re.compile(r'First\n(.*)Deaths', flags=re.DOTALL)
        list = re.findall(regex_1, texto)
        self.appearences = list[0]

    def get_deaths(self, texto):
        regex_1 = re.compile(r'Deaths(.*)Cast\n', flags=re.DOTALL)
        list = re.findall(regex_1, texto)
        self.deaths = list[0]

    def get_quote(self, texto):
        regex_1 = re.compile(r'quotes(.*)', flags=re.DOTALL)
        list = re.findall(regex_1, texto)
        self.quotes = list[0]

    def monta_texto_final(self):
        self.texto_final = self.title
        self.texto_final += self.plot
        self.texto_final += self.summary
        self.texto_final += self.appearences
        self.texto_final += self.deaths
        # self.texto_final += self.quotes

    def save_articles(self, to):
        with open(to + "/" + self.title + ".txt", 'w') as article_file:
            article_file.write(self.texto_final)

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
#         article.save_articles("first_processing/" + season_number[0])

article = ArticleReader("first_processing/season_1/Baelor.txt")