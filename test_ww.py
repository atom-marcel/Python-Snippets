from Statistics.ww import WebWords

if __name__ == "__main__":
    ww = WebWords(["https://www.youtube.com/watch?v=jqOvpVoWzas"])
    if ww.crawl():
        ww.analyze()
        ww.top = 30
        ww.print()