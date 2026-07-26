import spacy

nlp = spacy.load("en_core_web_sm")

doc = nlp("""John Doe Software Engineer OpenAI john@gmail.com""")


for ent in doc.ents:
    print(ent.text, ent.label_)