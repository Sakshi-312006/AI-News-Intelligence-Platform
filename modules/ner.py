import spacy


# Load pretrained English NLP model
nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    """
    Extract named entities from article text.
    """

    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "description": spacy.explain(ent.label_)
        })

    return entities