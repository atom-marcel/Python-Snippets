from bs4 import BeautifulSoup, ResultSet, Tag
from typing import List, Dict, Any
import json
import requests
import re

class WebWords(object):
    grammatik: Dict = \
    {
        "fuellwoerter": [
        "aber", "also", "am", "an", "auf", "auch", "aus", "bei", "bin", "bis", 
        "bist", "da", "dadurch", "daher", "darum", "das", "dass", "denn", 
        "der", "des", "deshalb", "die", "dies", "diese", "dieser", "dieses", 
        "doch", "dort", "du", "durch", "ein", "eine", "einem", "einen", 
        "einer", "eines", "einig", "einige", "einigem", "einigen", "einiger", 
        "einiges", "er", "es", "etwas", "euch", "euer", "eure", "für", "gegen", 
        "gewesen", "hab", "habe", "haben", "hat", "hatte", "hatten", "hier", 
        "hin", "hinter", "ich", "ihr", "ihre", "im", "in", "ist", "ja", "jede", 
        "jedem", "jeden", "jeder", "jedes", "jene", "jenem", "jenen", "jener", 
        "jenes", "jetzt", "kann", "kein", "keine", "kennen", "kennst", "können", 
        "könnt", "machen", "mein", "meine", "mit", "nach", "nachdem", "nein", 
        "nicht", "nichts", "noch", "nun", "nur", "ob", "oder", "ohne", "sehr", 
        "sein", "seine", "sich", "sie", "sind", "so", "solche", "solchem", 
        "solchen", "solcher", "solches", "soll", "sollen", "sondern", "sonst", 
        "über", "um", "und", "uns", "unser", "unsere", "unter", "viel", "vom", 
        "von", "vor", "während", "war", "waren", "warst", "was", "weg", "weil", 
        "weiter", "welche", "welchem", "welchen", "welcher", "welches", "wenn", 
        "werde", "werden", "wie", "wieder", "will", "wir", "wird", "wirst", 
        "wo", "wollen", "wollt", "wollte", "würde", "würden", "zu", "zum", 
        "zur", "zwar", "zwischen", "halb", "je", "wer"
        ],
        "ueberschriften_tags": ["h1", "h2", "h3", "h4", "h5", "h6", "title"],
        "text_tags": ["p", "span", "li", "div"],
        "satzzeichen": [",", ".", "!", "?", "\"", "&", "§", "/", ";", ":", "-", "*", "~", "+", "(", ")", "[", "]", "{", "}", "–", "|"]
    }

    websites: List[str]
    htmlString: ResultSet[Tag]
    onlyText: str
    wordList: List[str]
    filteredWords: List[str]
    bs: dict[str, BeautifulSoup]
    punctuation: List[str]
    searchTags: List[str]
    top: int = 10

    count: int
    countDictionary: Dict[str, int] = {}
    percentageDictionary: Dict[str, float] = {}

    def __init__(self, websites: List[str]) -> None:
        self.websites = websites
        self.bs = {}
        self.htmlString = []
        self.onlyText = ""

        j = self.grammatik
        self.filteredWords = j["fuellwoerter"]
        self.searchTags = j["ueberschriften_tags"] + j["text_tags"]
        self.punctuation = j["satzzeichen"]

    def crawl(self) -> bool:
        for website in self.websites:
            page = requests.get(website)
            
            if page.status_code != 200:
                return False
            
            content = page.content
            self.bs[website] = BeautifulSoup(content, "html.parser")
        
        return True

    def analyze(self):
        for website in self.bs.keys():
            for tag in self.searchTags:
                found = self.bs[website].find_all(tag)
                self.htmlString += found
                delimiter = " "
                self.onlyText += delimiter.join([x.string for x in self.htmlString if x.string])

        # self.wordList = re.split("\s+|\n", self.onlyText)
        for punc in self.punctuation:
            self.onlyText = self.onlyText.replace(punc, "")

        self.wordList = re.findall("\S+", self.onlyText, re.IGNORECASE)
        self.wordList = [x.lower() for x in self.wordList]

        for filteredWord in self.filteredWords:
            while filteredWord in self.wordList:
                self.wordList.remove(filteredWord)
        
        self.countWords()


    def countWords(self):
        self.count = len(self.wordList)

        for word in self.wordList:
            if word in self.countDictionary:
                self.countDictionary[word] += 1
            else:
                self.countDictionary[word] = 1

        for key in self.countDictionary.keys():
            self.percentageDictionary[key] = self.countDictionary[key] / self.count

    def printTop(self, skip:int = 0):
        countList = [(key, self.countDictionary[key]) for key in self.countDictionary.keys()]
        countList.sort(key=lambda x: x[1], reverse=True)

        percentageList = [(key, self.percentageDictionary[key]) for key in self.percentageDictionary.keys()]
        percentageList.sort(key=lambda x: x[1], reverse=True)

        # print("Anzahl der gezälten Wörter:")
        # for key, i in countList:
        #     print(f"{key} => {i}")

        # print("\nAnzahl des prozentualen Anteils der Wörter in Prozent")
        # for key, i in percentageList:
        #     print(f"{key} => {(i*100):2.2f}%")

        print(f"Top {self.top} der benutzen Wörter")
        for i in range(skip, self.top):
            if i < len(percentageList) and i < len(countList):
                print(f"{i+1-skip}. {percentageList[i][0][0].upper() + percentageList[i][0][1:]:25} \t {(percentageList[i][1]*100):2.2f}% \t ({countList[i][1]})")