"""N-Gram Text Analyser

As defined by Wikipedia: 
“In the fields of computational linguistics and probability, 
an n-gram is a contiguous sequence of n items from a given 
sample of text or speech.”"""

# https://importsem.com/build-an-n-gram-text-analyzer-for-seo-using-python/#Requirements-and-Assumptions




from keys import api_keys
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.util import ngrams
import requests
import json
import pandas as pd


url = "https://unitedpropertyservices.au/"

from urllib.request import urlopen


page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
paragraph = soup.find_all("p")
#print(soup.get_text())

# Extract the text from each paragraph
paragraph_texts = [p.text for p in paragraph] # paragraph_texts is a list including some unwanted signs

# Print extracted text
for text in paragraph_texts: # This for loop will print a body of text
    pass
#   print(text)


def grab_text(paragraph_texts):
    for text in paragraph_texts:
        return text


data = str(paragraph_texts) 
data = data.replace('\\','')
data = data.replace(',','')
data = data.replace('.','')
data = data.replace(';','')
data = data.replace('\xa0','')
data = data.replace('\n','')


def extract_ngrams(data, num):
    """Build N-Grams from text/data provided"""
    n_grams = ngrams(nltk.word_tokenize(data), num) # num refers to uni, bi and tri-gram eg. 2 = bi-gram
    gram_list = [ " ".join(grams) for grams in n_grams] # Join n-grams returned in single list

    for num in range(3): 
        query_tokens = nltk.pos_tag(gram_list)
        query_tokens = [x for x in query_tokens if x [1] in ['NN','NNS','NNP','NNPS','VBG','VBN']]
        query_tokens = [x[0] for x in query_tokens]
    return(query_tokens)




def kg(keywords):
    """Detect Entities from N-Grams"""
    kg_entities = []
    keys = api_keys

    for x in keywords:
        url = f"https://kgsearch.googleapis.com/v1/entities:search?query={x}&key={keys}&limit=1&indent=True"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data = payload)
        data = json.loads(response.text)

        try:
            getlabel = data["itemListElement"][0]["result"]["@type"]
            score = round(float(data["itemListElement"][0]["resultScore"]))
        except:
            score = 0
            getlabel = ["none"]

        labels = ""

        for item in getlabel:
            labels += item + " , "
        labels = labels[:-1].replace(",",", ")

        if labels != ["none"] and score > 500:
            kg_subset = []
            kg_subset.append(x)
            kg_subset.append(score)
            kg_subset.append(labels)

            kg_entities.append(kg_subset)
        return kg_entities


def surfer(entities,gram):
    """Gather Entity Search Metrics"""
    entities_type = [x[2] for x in entities]
    entities = [x[0] for x in entities]
    keywords = json.dumps(entities)

    url2 = 'https://db2.keywordsur.fr/keyword_surfer_keywords?country=us&keywords=' + keywords
    response2 = requests.get(url2,verify=True)
    seo_data = json.loads(response2.text)

    d = {'Keyword': [], 'Volume': [], 'CPC':[], 'Competition':[], 'Entity Types':[]}
    df = pd.DataFrame(data=d)
    counter=0

    for x in seo_data:

        if seo_data[x]["cpc"] == '':
            seo_data[x]["cpc"] = 0.0
        
        if seo_data[x]["competition"] == '':
            seo_data[x]["competition"] = 0.0

        new = {"Keyword":word,"Volume":str(seo_data[x]["search_volume"]),"CPC":"$"+str(round(float(seo_data[x]["cpc"]),2)),"Competition":str(round(float(seo_data[x]["competition"]),4)),'Entity Types':entities_type[counter]}
        df = df.append(new, ignore_index=True)
        counter +=1

    df.style.set_properties(**{'text-align': 'left'})
    df.sort_values(by=['Volume'], ascending=True)
    return df

keywords = extract_ngrams(data, 7)
entities = kg(keywords)
df = surfer(entities,2)

print(keywords)

#pd.to_csv(df)