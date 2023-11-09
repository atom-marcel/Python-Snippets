from Commandline.Menupy import Menu

def test1():
    print("Called test1")

def test2():
    print("Called test2")

if __name__ == "__main__":
    myMenu = Menu("TestMenu")
    myMenu.addCallable("test1", test1)
    myMenu.addCallable("test2", test2)

    myMenu.menuInteract()
