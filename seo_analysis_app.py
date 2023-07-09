"""The app will check the following:
Warnings, Title, Meta Description, Headings, Image Alt, Keywords"""

# resource video PART1 https://www.youtube.com/watch?v=1Y-x59e90Nw
# resource video PART2 https://youtu.be/j7TLgyTrtp8
# resource static https://pythonology.eu/build-an-seo-analyzer-using-python/


from bs4 import BeautifulSoup
import pandas as pd
import requests
from keys import api_keys
from var import res, soup, title, meta_d, url # Own Modules <----
from check_length_module import check_length
# nltk for natural language processing
import nltk
from nltk.tokenize import word_tokenize # Get a single token eg. single word from the text
nltk.download("stopwords") # Words that aren't helpful when analysing keywords eg. the
nltk.download("punkt")


# Webpage to analyse
# For Streamlit url = input(f"Enter url to run analysis: ")
url = "https://unitedpropertyservices.au/"


def analyse_url(url):
    """Analyse headings, keywords & alt attribute in images"""
    warning = [] # Warning may including missing tile, meta-content, alt etc...
    ok = []      # Includes good titles, headings, descriptions etc...




    if title:  # Add title to ok list if title exists
        ok.append(f"Title exists: {title}")
        check_length(title)
    else:      # If no title then add to warning list  
        warning.append(f"Title is missing!")




    if meta_d: # Add meta description to ok list if title exists
        ok.append(f"Meta Description exists: {meta_d}")
        check_length(meta_d)
    else:
        warning.append(f"Meta Description is missing")




    hs = ["h1", "h2", "h3", "h4", "h5", "h6"] # Grab Headings
    h_tags = []


    for h in soup.find_all(hs): 
        ok.append(f"{h.name}-->{h.text.strip()}")
        h_tags.append(h.name)
    if "h1" not in h_tags:
        warning.append("No H1 found!")
    



    for i in soup.find_all("img", alt=" "): # Extract the images without Alt
        warning.append(f"No Alt: {i}")
    else:
        print("All images contain 'Alt Attribute'.\n")

    # Extract keywords
    bod = soup.find("body").text # Grab text from body of the HTML
    # Add words inside list 
    words = [i.lower() for i in word_tokenize(bod)] # Return i for i in word-tokenize
    
    # Grab a list of English stopwords (actual words not from url)
    sw = nltk.corpus.stopwords.words("english")
    keywords = []

    for i in words:                     # If found in words variable, stop words are to be excluded.
        if i not in sw and i.isalpha(): # isalpha stands for actual words and not symbols etc...
            keywords.append(i)
    
     

    
    freq = nltk.FreqDist(keywords) # Check frequency distribution of keywords

    print(f"Keywords FreqDist: {freq.most_common(10)}") # Check most common top 10
    print(f"OK: {ok}")
    print(f"WARNING: {warning}")



analyse_url(url)

