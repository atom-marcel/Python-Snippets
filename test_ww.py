from Statistics.ww import WebWords

if __name__ == "__main__":
    ww = WebWords(["https://www.tagesschau.de/"])
    if ww.crawl():
        ww.analyze()
        ww.top = 30
        ww.printTop()