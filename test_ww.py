from Statistics.ww import WebWords

if __name__ == "__main__":
    ww = WebWords(["https://www.tagesschau.de/"])
    assert ww.crawl(), "Crawling failed"
    ww.analyze()
    ww.top = 30
    ww.printTop()