
""" Var module allows both functions on different files
to access the same variables """


from bs4 import BeautifulSoup
import requests

# Getting the url text
res = requests.get(url).text

# Parse the HTML content
soup = BeautifulSoup(res, "html.parser")

# Extract the Title & Meta Description
title = soup.find('title').text # .text removes tags eg. <title>
# attrs={"name": "description"} Looks specifically for Meta description with attribute
meta_d = soup.find("meta", attrs={"name": "description"})["content"] # ["content"] ensures only meta_d content is displayed without tags 
