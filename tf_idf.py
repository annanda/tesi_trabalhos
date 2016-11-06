import glob
import os
import nltk


def remove_meaningless_tokens(tokens):
    meaningless_tokens = [".", ",", "'", ":", "!", ";",
                          "?", "]", "[", "&", "-", "...",
                          ")", "(", "``", "--", "'s", "i.e",
                          "'d",   # he'd, they'd
                          "'m",   # I'm
                          "''",   # não aparece no texto, mas tem um token com isso
                          "'ve",  # they've
                          "'re",  # they're
                          "n't",  # doesn't
                          "'ll",  # they'll
                          ]

    return [token for token in tokens if token not in meaningless_tokens]


def normalize_tokens(tokens):
    normalized = []
    for token in tokens:
        token = token.lower()

        # para má tokenização, principalmente no começo de dialogos como '......'
        # wed., 'that, 'gift, 'Lady, sept., 'take,
        # 'shove, 'Knight, 'scythe, Stannis', Daenerys',
        # 'doubtless, 'Littlefinger, 'a, 'no, 'he, 'the, 'his
        token = token.strip(".'")

        # remove possessivo
        if token.endswith("'s"):
            token = token[:-2]

        normalized.append(token)

    return normalized


def tokenize_document(text):
    lines = text.split("\n")

    sentences = []
    for line in lines:
        sentences += nltk.sent_tokenize(line)

    document_tokens = []

    for sentence in sentences:
        sentence_tokens = nltk.word_tokenize(sentence)

        t.extend(document_tokens)

        sentence_tokens = remove_meaningless_tokens(sentence_tokens)
        sentence_tokens = normalize_tokens(sentence_tokens)
        document_tokens.extend(sentence_tokens)

    return document_tokens


t = []
t_c = []
all_text = ""

docs = {}
seasons_files = glob.glob("pre_processed_documents/*")
for season in seasons_files:
    season_name = os.path.basename(season)

    episodes_files = glob.glob(season + "/*.txt")
    for episode_file in episodes_files:
        episode_name = os.path.basename(episode_file)

        with open(episode_file, 'r', encoding='utf-8') as input_file:
            episode_text = input_file.read()
            all_text += episode_text

        document_name = season_name + "_" + episode_name
        document_tokens = tokenize_document(episode_text)

        t_c.extend(document_tokens)

        docs[document_name] = document_tokens

print(len(set(t_c)))

# with open("all_text.txt", "w+", encoding='utf-8') as output_file:
#     output_file.write(all_text)

# for _ in set(t_c):
#     if len(_) == 3:
#         print(_)
