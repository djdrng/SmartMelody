
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline('sentiment-analysis', 
                    model='arpanghoshal/EmoRoBERTa')


# To use from a different folder: 
#
# from parsing_and_analysis.main import analyzeText
#
# print(analyzeText("harry potter is great"))

def analyzeText(input_text):
    emotion_labels = emotion(input_text)
    return emotion_labels


