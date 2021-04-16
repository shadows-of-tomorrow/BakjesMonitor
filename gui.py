import threading
import tkinter as tk
from engine import Engine


class GUI:

    def __init__(self, engine):
        self.engine = engine
        self.top_left = 0
        self._construct_main_window()

    def _construct_main_window(self):
        # Construct main window.
        self.main_window = tk.Tk()

        # Configure window settings.
        self.main_window.title("Bakjes Monitor v1.0")
        self.main_window.geometry("300x300")
        self.main_window.configure(bg='white')

        # Add alu baba logo image.
        background_img = tk.PhotoImage(file="./img/icons/alubaba.png")
        background_label = tk.Label(self.main_window, image=background_img, bg='white')
        background_label.place(x=0, y=0)
        background_label.image = background_img

        # Add buttons to main window.
        self._add_buttons()

        # Add "top left" lane monitor.
        top_left_label = tk.Label(self.main_window, text="--", font=("Arial", 20), bg="white", fg="black",
                                  borderwidth=2, relief="solid", width=3)
        top_left_label.place(x=100, y=120)

        # Add "top right" lane monitor.
        top_right_label = tk.Label(self.main_window, text="--", font=("Arial", 20), bg="white", fg="black",
                                   borderwidth=2, relief="solid", width=3)
        top_right_label.place(x=160, y=120)

        # Add "bottom left" lane monitor.
        bottom_left_label = tk.Label(self.main_window, text="--", font=("Arial", 20), bg="white", fg="black",
                                     borderwidth=2, relief="solid", width=3)
        bottom_left_label.place(x=100, y=170)

        # Add "bottom right" lane monitor.
        bottom_right_label = tk.Label(self.main_window, text="--", font=("Arial", 20), bg="white", fg="black",
                                      borderwidth=2, relief="solid", width=3)
        bottom_right_label.place(x=160, y=170)

        # Add status label.
        monitoring_text = tk.Label(self.main_window, text="Status:", bg="white")
        monitoring_text.place(x=10, y=250)
        monitoring_label = tk.Label(self.main_window, text="Paused", fg="red", bg="white")
        monitoring_label.place(x=60, y=250)

        # Add alarm label.
        alarm_text = tk.Label(self.main_window, text="Alarm:", bg="white")
        alarm_text.place(x=10, y=270)
        alarm_label = tk.Label(self.main_window, text="Off", fg="green", bg="white")
        alarm_label.place(x=60, y=270)

        # Add dynamic updating.
        def update_values():
            # Update digits.
            top_left_label['text'] = self._digit_to_str(self.engine.digits_old['top_left'])
            top_right_label['text'] = self._digit_to_str(self.engine.digits_old['top_right'])
            bottom_left_label['text'] = self._digit_to_str(self.engine.digits_old['bottom_left'])
            bottom_right_label['text'] = self._digit_to_str(self.engine.digits_old['bottom_right'])

            # Update status.
            if not self.engine.looping:
                monitoring_label['text'] = "Paused"
                monitoring_label['fg'] = 'red'
            else:
                monitoring_label['text'] = "Active"
                monitoring_label['fg'] = 'green'

            # Update alarm.
            if self.engine.alarm_on:
                alarm_label['text'] = 'On'
                alarm_label['fg'] = 'red'
            else:
                alarm_label['text'] = 'Off'
                alarm_label['fg'] = 'green'

            self.main_window.after(10, update_values)

        update_values()

    def _digit_to_str(self, digit):
        if digit <= 9:
            return "0" + str(digit)
        else:
            return str(digit)

    def _add_buttons(self):
        # Add play button.
        play_button_img = tk.PhotoImage(file="./img/icons/play.png")
        play_button = tk.Button(self.main_window, command=self.play, image=play_button_img)
        play_button.place(x=210, y=250)
        play_button.image = play_button_img

        # Add pause button.
        pause_button_img = tk.PhotoImage(file="./img/icons/pause.png")
        pause_button = tk.Button(self.main_window, command=self.pause, image=pause_button_img)
        pause_button.place(x=250, y=250)
        pause_button.image = pause_button_img

        # Add settings button.
        settings_button_img = tk.PhotoImage(file="./img/icons/settings.png")
        settings_button = tk.Button(self.main_window, command=self.settings, image=settings_button_img)
        settings_button.place(x=170, y=250)
        settings_button.image = settings_button_img

    def _construct_settings_window(self):
        # Construct settings window.
        settings_window = tk.Toplevel()

        # Configure windows settings.
        settings_window.title("Settings")
        settings_window.geometry("300x300")

        # Add wait time entry.
        wait_time_label = tk.Label(settings_window, text="Alarm Time:")
        wait_time_label.place(x=10, y=10)
        wait_time_entry = tk.Entry(settings_window)
        wait_time_entry.place(x=100, y=10)

        # Add step time entry.
        step_time_label = tk.Label(settings_window, text="Step Time:")
        step_time_label.place(x=10, y=40)
        step_time_entry = tk.Entry(settings_window)
        step_time_entry.place(x=100, y=40)

        # Add stop steps entry.
        stop_steps_label = tk.Label(settings_window, text="Stop Steps:")
        stop_steps_label.place(x=10, y=70)
        stop_steps_entry = tk.Entry(settings_window)
        stop_steps_entry.place(x=100, y=70)

        # Add switch ID entry.
        switch_id_label = tk.Label(settings_window, text="Switch ID:")
        switch_id_label.place(x=10, y=100)
        switch_id_entry = tk.Entry(settings_window)
        switch_id_entry.place(x=100, y=100)

        # Add lane checkboxes.
        lane_label = tk.Label(settings_window, text="Lanes:")
        lane_label.place(x=10, y=140)
        top_left_var = tk.IntVar()
        top_left_box = tk.Checkbutton(settings_window, text="Top Left", variable=top_left_var)
        top_left_box.place(x=100, y=140)
        top_right_var = tk.IntVar()
        top_right_box = tk.Checkbutton(settings_window, text="Top Right", variable=top_right_var)
        top_right_box.place(x=100, y=160)
        bottom_left_var = tk.IntVar()
        bottom_left_box = tk.Checkbutton(settings_window, text="Bottom Left", variable=bottom_left_var)
        bottom_left_box.place(x=100, y=180)
        bottom_right_var = tk.IntVar()
        bottom_right_box = tk.Checkbutton(settings_window, text="Bottom Right", variable=bottom_right_var)
        bottom_right_box.place(x=100, y=200)

        # Store settings function.
        def _store_settings():
            # Update time engine settings.
            if not wait_time_entry.get() == "":
                self.engine.wait_time = float(wait_time_entry.get())
            if not step_time_entry.get() == '':
                self.engine.step_time = float(step_time_entry.get())
            if not stop_steps_entry.get() == '':
                self.engine.stop_steps = int(stop_steps_entry.get())

            # Update switch settings.
            if not switch_id_entry.get() == "":
                self.engine.reset_switch(switch_id_entry.get())

            # Update lane engine settings.
            self.engine.lanes = []
            if top_left_var.get() == 1:
                self.engine.lanes.append('top_left')
            if top_right_var.get() == 1:
                self.engine.lanes.append('top_right')
            if bottom_left_var.get() == 1:
                self.engine.lanes.append('bottom_left')
            if bottom_right_var.get() == 1:
                self.engine.lanes.append('bottom_right')
            settings_window.destroy()

        # Add store settings button.
        store_button_img = tk.PhotoImage(file="./img/icons/check.png")
        store_button = tk.Button(settings_window, command=_store_settings, image=store_button_img)
        store_button.image = store_button_img
        store_button.place(x=250, y=250)

        settings_window.mainloop()

    def _threaded_engine_run(self):
        thread = threading.Thread(target=self.engine.run)
        thread.start()

    def play(self):
        self.engine.looping = True
        self._threaded_engine_run()

    def pause(self):
        self.engine.looping = False

    def settings(self):
        self.engine.looping = False
        self._construct_settings_window()

    def run(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    engine = Engine()
    gui = GUI(engine)
    gui.run()
