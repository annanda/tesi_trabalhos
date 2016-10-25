import re
import glob
import os.path


class ArticleReader:
    def __init__(self, from_path):
        self.texto_pre_processado = None
        with open(from_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            lines = [line.strip('\n').strip() for line in lines]
            lines = [line for line in lines if line]

            for i, line in enumerate(lines):
                clean = line
                clean = clean.replace("—", " - ")
                clean = clean.replace("…", "... ")
                clean = clean.replace("ʼ", "'")
                clean = clean.replace("’", "'")  # não é o mesmo do que o de cima
                clean = clean.replace("–", " - ")
                clean = clean.replace("―", " - ")
                clean = clean.replace("“", "\"")
                clean = clean.replace("”", "\"")
                clean = clean.replace("\u200B", "")
                lines[i] = clean

            for i, line in enumerate(lines):
                if line.endswith("Edit"):
                    lines[i] = line[:-4].strip()

            captured = []
            capture = False
            for line in lines:
                if line == "Plot":
                    capture = True

                if line == "Summary":
                    continue

                if line == "Appearances" or line == "Recap":
                    capture = False

                if capture:
                    captured.append(line)

            captured = captured[1:]  # remove PlotEdit

            for line in captured:
                for char in line:
                    if ord(char) > 256:
                        i += 1
                        print("({0}) is number {1} appears in {2}".format(char, ord(char), line))

            self.texto_pre_processado = "\n".join(captured)

    def save_pre_processed_file(self, to):
        with open(to, 'w+', encoding="utf-8") as file:
            file.write(self.texto_pre_processado)


seasons_files = glob.glob("raw_documents/*")
for season in seasons_files:
    season_name = os.path.basename(season)

    episodes_files = glob.glob(season + "/*.txt")
    for episode in episodes_files:
        episode_name = os.path.basename(episode)
        save_dir = os.path.join("pre_processed_documents", season_name)
        os.makedirs(save_dir, exist_ok=True)
        article = ArticleReader(episode)
        article.save_pre_processed_file(os.path.join(save_dir, episode_name))
