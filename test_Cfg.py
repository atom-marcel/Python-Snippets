from Data_Manipulation.cfg import Cfg

if __name__ == "__main__":
    cfg = Cfg("test.cfg")
    cfg.loadFile()
    cfg.rawStringToInformation()
    cfg.information["Test"] = {}
    cfg.information["Test"]["TEst1"] = "1"
    cfg.information["Test"]["test2"] = "2"
    cfg.informationToRawString()
    cfg.path = "testOut.cfg"
    cfg.saveFile()
    print(cfg.rawString)