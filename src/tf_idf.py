import glob
import os
from collections import Counter
import sys
import nltk
import math


def remove_meaningless_tokens(tokens):
    meaningless_tokens = [".", ",", "'", ":", "!", ";",
                          "?", "]", "[", "&", "-", "...",
                          ")", "(", "``", "--", "'s", "i.e",
                          "'d",  # he'd, they'd
                          "'m",  # I'm
                          "''",  # não aparece no texto, mas tem um term com isso
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

        sentence_tokens = remove_meaningless_tokens(sentence_tokens)
        sentence_tokens = normalize_tokens(sentence_tokens)
        document_tokens.extend(sentence_tokens)

    return document_tokens


def calculate_score(dindex, tindexes, tf_idf):
    result = 0
    for tindex in tindexes:
        result += tf_idf[tindex][dindex]

    return result


def query(search_query):
    terms = []
    documents = []
    freq_by_document = {}
    seasons_files = glob.glob("../generated/pre_processed_documents/*")
    for season in seasons_files:
        season_name = os.path.basename(season)

        episodes_files = glob.glob(season + "/*.txt")

        # episodes_files = ["experiments/tfidf1.txt", "experiments/tfidf2.txt", "experiments/tfidf3.txt"]

        for episode_file in episodes_files:
            episode_name = os.path.basename(episode_file)

            with open(episode_file, 'r', encoding='utf-8') as input_file:
                episode_text = input_file.read()

            document_name = season_name + "_" + episode_name
            document_tokens = tokenize_document(episode_text)

            terms.extend(document_tokens)
            freq_by_document[document_name] = Counter(document_tokens)
            documents.append(document_name)

    terms = list(set(terms))  # tira repetidos
    idf_by_term = dict()
    tf_idf = []

    for term in terms:
        tf = []
        number_of_documents_with_term = 0
        for document in documents:
            freq = freq_by_document[document][term]

            if freq > 0:
                number_of_documents_with_term += 1

            tf.append(freq)

        idf_by_term[term] = math.log(len(documents) / number_of_documents_with_term)

        tf = [tf_t * idf_by_term[term] for tf_t in tf]

        tf_idf.append(tf)

    document_tokens = tokenize_document(search_query)
    existing_terms = set(terms).intersection(document_tokens)  # remove termos que não existem nos documentos

    scores = []
    for i, document in enumerate(documents):
        tindexes = []
        for term in existing_terms:
            tindexes.append(terms.index(term))

        score = calculate_score(i, tindexes, tf_idf)
        scores.append((score, document))

    documents = [score[1] for score in sorted(scores, key=lambda s: s[0], reverse=True)][:5]

    for document in documents:
        print(document)


if __name__ == "__main__":
    search_query = " ".join(sys.argv[1:])
    query(search_query)
