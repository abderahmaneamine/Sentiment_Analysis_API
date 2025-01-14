from transformers import pipeline
nlp = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
def generate(text: str):
    sentiment = nlp(text)
    return sentiment
