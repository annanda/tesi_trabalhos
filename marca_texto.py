import jsonpickle
import glob
import os


def tag_text(text, entities):
    sorted_entities = sorted(entities, key=lambda it: len(it.original), reverse=True)

    for i, entity in enumerate(sorted_entities):
        entity_name = entity.original
        entity_name = entity_name.replace(" 's", "'s")
        text = text.replace(entity_name, "<<{0}>>".format(i))

    for i, entity in enumerate(sorted_entities):
        text = text.replace("<<{0}>>".format(i),
                            "<en name='{0}' type='{1}'>{2}</en>".format(entity.canonico,
                                                                        entity.classification,
                                                                        entity.original))

    return text


with open("classifica_e_reune.json", 'r') as file:
    entities = jsonpickle.decode(file.read())

seasons_files = glob.glob("pre_processed_documents/*")
for season in seasons_files:
    season_name = os.path.basename(season)

    episodes_files = glob.glob(season + "/*.txt")
    for episode_file in episodes_files:
        episode_name = os.path.basename(episode_file)
        save_dir = os.path.join("tagged_documents", season_name)
        os.makedirs(save_dir, exist_ok=True)

        with open(episode_file, 'r', encoding='utf-8') as input:
            episode_text = input.read()

        tagged_text = tag_text(episode_text, entities)

        with open(os.path.join(save_dir, episode_name), 'w+', encoding='utf-8') as output:
            output.write(tagged_text)
