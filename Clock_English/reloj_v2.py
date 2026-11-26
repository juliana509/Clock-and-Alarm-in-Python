import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import pygame.mixer   # alarma.mp3
import os

class ClockApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Delgado Labrovich Juliana - TKinder Clock App")
        self.geometry("650x460")
        self.resizable(False, False)
        self.configure(bg="black")

        # Initialize the Pygame mixer for sound
        try:
            pygame.mixer.init()
        except Exception as e:
            messagebox.showerror("Audio Initialization Error", f"Could not initialize the Pygame audio system: {e}")
            print(f"Error initializing pygame.mixer: {e}")

        # Store the alarm time
        self.alarm_time = None

        self.create_widgets()
        self.update_datetime()

    def create_widgets(self):
        """Create and pack the widgets."""
        # Date label
        self.date_label = tk.Label(
            self,
            font=("Arial", 25, "bold"),
            bg="black",
            fg="cyan"
        )
        self.date_label.pack(pady=10)

        # Time label
        self.time_label = tk.Label(
            self,
            font=("Arial", 70, "bold"),
            bg="black",
            fg="lime green"
        )
        self.time_label.pack(expand=True)

        # Alarm
        alarm_frame = tk.Frame(self, bg="black")
        alarm_frame.pack(pady=20)

        # Label for the input field
        alarm_label = tk.Label(
            alarm_frame,
            text="Study alarm for finals (HH:MM):",
            font=("Arial", 14),
            bg="black",
            fg="white"
        )
        alarm_label.pack(pady=5)

        # Input field for the alarm time
        self.alarm_entry = tk.Entry(
            alarm_frame,
            font=("Arial", 14),
            width=8,
            bg="gray20",
            fg="white",
            insertbackground="white" # Cursor color
        )
        self.alarm_entry.pack(pady=5)

        # Button to set the alarm
        set_alarm_button = tk.Button(
            alarm_frame,
            text="Set Alarm",
            font=("Arial", 12, "bold"),
            bg="lime green",
            fg="black",
            command=self.set_alarm
        )
        set_alarm_button.pack(pady=5)

        # Button to stop the alarm manually
        stop_alarm_button = tk.Button(
            alarm_frame,
            text="Turn off Alarm",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            command=self.stop_alarm
        )
        stop_alarm_button.pack(pady=5)

        # Label to show the alarm status
        self.alarm_status_label = tk.Label(
            self,
            text="Alarm off",
            font=("Arial", 12),
            bg="black",
            fg="red"
        )
        self.alarm_status_label.pack(pady=5)

    def update_datetime(self):
        """
        Update the date and time, and check the alarm.
        """
        now = datetime.now()

        # Formatted time and date
        current_time_str = now.strftime("%H:%M:%S")

        # Date format: weekday, month day, year
        current_date_str = now.strftime("%A, %B %d, %Y")

        self.time_label.config(text=current_time_str)
        self.date_label.config(text=current_date_str)

        # Check the alarm
        if self.alarm_time and now.strftime("%H:%M") == self.alarm_time:
            self.trigger_alarm()

        # Call this function every second (1000 milliseconds)
        self.after(1000, self.update_datetime)

    def set_alarm(self):
        """
        Save the alarm time entered by the user.
        """
        alarm_input = self.alarm_entry.get()

        # Validate the input format (HH:MM)
        try:
            # Parse the time to check that it has the correct format
            datetime.strptime(alarm_input, "%H:%M")
            self.alarm_time = alarm_input
            self.alarm_entry.delete(0, tk.END)
            self.alarm_status_label.config(text=f"Alarm set for {self.alarm_time}", fg="lime green")
            messagebox.showinfo("Alarm", f"Alarm set for {self.alarm_time}!")

        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Use HH:MM (e.g., 14:30).")
            self.alarm_status_label.config(text="Alarm off (Invalid format)", fg="red")
            self.alarm_time = None

    def play_alarm_sound(self):
        """
        Play an alarm sound file using pygame.mixer.
        Make sure an audio file (e.g., 'alarma.mp3' or 'alarma.wav') is in the same directory.
        """
        try:
            # Get the absolute path of the directory containing this script
            script_dir = os.path.dirname(__file__)
            # Build the full path to the sound file
            sound_file_path = os.path.join(script_dir, 'alarma.mp3')

            # Load the sound file
            pygame.mixer.music.load(sound_file_path)
            # Play the sound in a continuous loop until it is stopped
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            messagebox.showerror("Sound Error", f"Could not play the sound: {e}\nMake sure 'alarma.mp3' exists in the same folder as the script and is compatible with Pygame.")
            print(f"Error playing sound with pygame.mixer: {e}")

    def trigger_alarm(self):
        """
        Show a notification and play the sound when the alarm goes off.
        The alarm is deactivated immediately afterward to prevent repeated triggers.
        """
        if self.alarm_time is not None:
            self.play_alarm_sound()
            messagebox.showinfo("ALARM!", "It's time to study for your final!")
            # The sound will keep playing until the user stops it manually.
            self.alarm_time = None
            self.alarm_status_label.config(text="Alarm: Ringing...", fg="orange")

    def stop_alarm(self):
        """
        Stop the alarm sound and deactivate the alarm.
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            messagebox.showinfo("Alarm", "Alarm stopped manually. Good luck studying!")

        self.alarm_time = None
        self.alarm_status_label.config(text="Alarm off", fg="red")

if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()