import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize

#Key words extraction
from keybert import KeyBERT
kw_model = KeyBERT()
def extract(doc):
  
  KeyBERT= kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2) )
  KeyBERT_ans=[]

  for i in range(len(KeyBERT)):
    KeyBERT_ans.append(KeyBERT[i][0])
  return(KeyBERT_ans)

#T5 model
from transformers import AutoModelWithLMHead, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")

from transformers import AutoModelWithLMHead, AutoTokenizer


def get_question(answer, context, max_length=64):
  input_text = "answer: %s  context: %s </s>" % (answer, context)
  features = tokenizer([input_text], return_tensors='pt')

  output = model.generate(input_ids=features['input_ids'],
               attention_mask=features['attention_mask'],
               max_length=max_length)

  return tokenizer.decode(output[0],skip_special_tokens=True)

#QA pipeline
from transformers import pipeline
question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')

"""##T5 model"""
"""
from transformers import T5ForConditionalGeneration,T5Tokenizer

#T5 model size on disk ~ 900 MB
t5_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1')
t5_tokenizer = T5Tokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')

def get_question(sentence,answer):
  text = "context: {} answer: {}".format(sentence,answer)

  max_len = 512
  encoding = t5_tokenizer.encode_plus(text,max_length=max_len, pad_to_max_length=False,truncation=True, return_tensors="pt")

  input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

  outs = t5_model.generate(input_ids=input_ids,
                                  attention_mask=attention_mask,
                                  early_stopping=True,
                                  num_beams=5,
                                  num_return_sequences=1,
                                  no_repeat_ngram_size=2,
                                  max_length=300)


  dec = [t5_tokenizer.decode(ids,skip_special_tokens=True) for ids in outs]


  Question = dec[0].replace("question:","")
  Question= Question.strip()
  return Question

"""
