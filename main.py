import tkinter as tk
from datetime import datetime, timedelta
import pygame
from pygame import mixer 

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer App")
        master.resizable(False, False)

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x_coordinate = (screen_width - master.winfo_reqwidth()) // 2
        y_coordinate = (screen_height - master.winfo_reqheight()) // 2

        master.geometry(f'+{x_coordinate}+{y_coordinate}')

        self.duration_entry = tk.Entry(master)
        self.duration_entry.pack(pady=10)

        self.start_button = tk.Button(master, text="Start Timer", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Timer", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack()

        self.switch_format_button = tk.Button(master, text="Switch Format", command=self.switch_format)
        self.switch_format_button.pack()

        self.time_label = tk.Label(master)
        self.time_label.pack(pady=5)

        self.unit_labels = [
            tk.Label(master, text="Hours"),
            tk.Label(master, text="Minutes"),
            tk.Label(master, text="Seconds"),
        ]

        for label in self.unit_labels:
            label.pack()

        self.is_24_hour_format = True
        self.end_time = None
        self.paused_time = None

        mixer.init()
        self.alarm_sound = pygame.mixer.Sound('samsung_alarm.mp3')

        self.update_display()

    def update_display(self):
        if self.end_time or self.paused_time:
            remaining_time = (self.end_time - datetime.now()) if self.end_time else (self.paused_time - datetime.now())
            format_str = '%H:%M:%S' if self.is_24_hour_format else '%I:%M:%S %p'

            font_size = 48 if remaining_time.total_seconds() > 3600 else 24
            self.time_label.config(font=('Helvetica', font_size))

            formatted_time = str(remaining_time).split(".")[0]
            self.time_label.config(text=formatted_time)

            hours, remainder = divmod(remaining_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)

            self.unit_labels[0].config(text=f"{int(hours)} Hours")
            self.unit_labels[1].config(text=f"{int(minutes)} Minutes")
            self.unit_labels[2].config(text=f"{int(seconds)} Seconds")

            if remaining_time.total_seconds() <= 0:
                self.time_label.config(text="00:00:00")
                for label in self.unit_labels:
                    label.config(text="")
                self.end_time = None

                self.play_alarm()

                self.start_button.config(state=tk.NORMAL)

                self.stop_button.config(state=tk.DISABLED)

            elif self.paused_time:
                self.stop_button.config(state=tk.NORMAL)
        else:
            current_time = datetime.now().time()
            format_str = '%H:%M:%S' if self.is_24_hour_format else '%I:%M:%S %p'
            self.time_label.config(font=('Helvetica', 48))
            self.time_label.config(text=current_time.strftime(format_str))
            for label in self.unit_labels:
                label.config(text="")
            self.stop_button.config(state=tk.DISABLED)

        self.master.after(1000, self.update_display)

    def start_timer(self):
        try:
            timer_duration = int(self.duration_entry.get()) * 60

            self.end_time = datetime.now() + timedelta(seconds=timer_duration)

            self.start_button.config(state=tk.DISABLED)

            self.stop_button.config(state=tk.NORMAL)
        except ValueError:
            print("Please enter a valid duration in minutes.")

    def stop_timer(self):
        pygame.mixer.stop()

        self.start_button.config(state=tk.NORMAL)

        self.end_time = None
        self.paused_time = None

    def play_alarm(self):
        pygame.mixer.Channel(0).play(self.alarm_sound, loops=-1)

    def switch_format(self):
        self.is_24_hour_format = not self.is_24_hour_format

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
