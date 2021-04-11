import threading
import tkinter as tk
from engine import Engine


class GUI:

    def __init__(self, engine):
        self.engine = engine
        self.window = tk.Tk()
        self._style_window()

    def _style_window(self):
        self.window.title("Bakjes Monitor v1.0")
        self.window.geometry("300x300")
        self.window.configure(bg='white')
        background_img = tk.PhotoImage(file="./img/alubaba.png")
        background_label = tk.Label(self.window, image=background_img)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_img

    def _threaded_engine_run(self):
        thread = threading.Thread(target=self.engine.run)
        thread.start()

    def loop_on(self):
        self.engine.looping = True
        self._threaded_engine_run()

    def loop_off(self):
        self.engine.looping = False

    def kill(self):
        self.window.destroy()

    def settings(self):
        print("Settings!")

    def run(self):
        button_on = tk.Button(self.window, text='Aan', command=self.loop_on, height=1, width=10)
        button_on.place(x=110, y=60)
        button_off = tk.Button(self.window, text='Pauze', command=self.loop_off, height=1, width=10)
        button_off.place(x=210, y=130)
        button_kill = tk.Button(self.window, text='Uit', command=self.kill, height=1, width=10)
        button_kill.place(x=10, y=130)
        button_settings = tk.Button(self.window, text='Instellingen', command=self.settings, height=1, width=10)
        button_settings.place(x=110, y=210)
        self.window.mainloop()


if __name__ == "__main__":
    engine = Engine()
    gui = GUI(engine)
    gui.run()
