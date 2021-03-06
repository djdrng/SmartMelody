
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline('sentiment-analysis', 
                    model='arpanghoshal/EmoRoBERTa')

# takes in a string of text and outputs it's sentiment analysis as an dictionary array ie:
# [{'label': 'admiration', 'score': 0.9948461055755615}]
def analyzeText(input_text):
    """
    To call this function from a different folder: 
    from parsing_and_analysis import analyzeText
    print(analyzeText("harry potter is great"))
    """
    emotion_labels = emotion(input_text)
    return emotion_labels
