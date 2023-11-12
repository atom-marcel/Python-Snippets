from bs4 import BeautifulSoup, ResultSet, Tag
from typing import List, Dict, Any
import json
import requests
import re

class WebWords(object):
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

        with open("./Statistics/grammatik.json", "r") as f:
            j = json.loads(f.read())
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

    def print(self):
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
        for i in range(self.top):
            if i < len(percentageList) and i < len(countList):
                print(f"{i+1}. {percentageList[i][0][0].upper() + percentageList[i][0][1:]:25} \t {(percentageList[i][1]*100):2.2f}% \t ({countList[i][1]})")