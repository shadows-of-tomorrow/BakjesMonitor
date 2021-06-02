from utils.dummies import DummyEngine
from brain.gui import GUI

if __name__ == "__main__":
    engine = DummyEngine("D:/alu-robo/pi3/")
    gui = GUI(engine=engine)
    gui.run()
