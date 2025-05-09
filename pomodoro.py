from tkinter import *
from tkinter import ttk, messagebox, PhotoImage
from play_ffmpeg import PlayFFMPEG

TESTING = False

# By default this will run 4 work and short
# rest cycles back to back before a long rest.
PHASES = [
    [25, "WORK"],
    [5, "SHORT REST 1"],
    [25, "WORK"],
    [5, "SHORT REST 2"],
    [25, "WORK"],
    [5, "SHORT REST 3"],
    [25, "WORK"],
    [5, "SHORT REST 4"],
    [25, "WORK"],
    [15, "LONG REST"],
]


class PomodoroTimer(Tk):
    """
    Class for implementing a simple Pomodoro timer
    """

    frame = None
    phases = None
    clock = None
    phase_index = 0
    clock_running = True
    img = None

    # UI components
    clock_label, phase_label, start, reset = None, None, None, None

    # Custom FFMPEG library
    ffmpeg = PlayFFMPEG()

    def __init__(self, phases: list) -> None:
        super().__init__()

        self.title("Mini Pomodoro")
        self.frame = ttk.Frame(self, padding=10)
        self.frame.grid()
        self.phases = phases
        # The phase array is in minutes, convert all the values to seconds.
        if not TESTING:
            for i in range(len(self.phases)):
                self.phases[i][0] *= 60

        # Set default value of the clock.
        self.clock = self.phases[self.phase_index][0]

        # Create the title and icon image.
        self.img = PhotoImage(file="tomato.png")
        self.iconphoto(False, self.img)
        ttk.Label(self.frame, image=self.img).grid(column=0, row=0)
        self.clock_label = ttk.Label(self.frame, text=self.seconds_to_clock(self.clock))
        self.phase_label = ttk.Label(
            self.frame, text=f"PHASE: {self.phases[self.phase_index][1]}"
        )
        self.phase_label.grid(column=0, row=1)
        self.clock_label.grid(column=0, row=2, pady=(0, 20))
        ttk.Button(self.frame, text="Start", command=self._start_counter).grid(
            column=0, row=3, padx=50
        )
        ttk.Button(self.frame, text="Reset", command=self._reset_counter).grid(
            column=0, row=4
        )
        ttk.Button(self.frame, text="Quit", command=self.destroy).grid(column=0, row=5)

    def _iterate_counter(self) -> None:
        """
        Iterate the counter, update UI, and move to next phase.
        """
        if self.clock_running:
            print("Counter running is true")
            if self.clock == 0:
                print("Next phase")
                previous_phase = self.phase_index
                self.phase_index += 1
                self.phase_index %= len(PHASES)
                self.clock_running = False
                self.ffmpeg.play_sound("alert_sound.wav")
                messagebox.showinfo(
                    "NEW PHASE!",
                    f"{self.phases[previous_phase][1]} has ended.\nPress start to begin new phase, {self.phases[self.phase_index][1]}",
                )
                self._reset_counter()
                return
            self.clock -= 1
            self.clock_label.config(text=self.seconds_to_clock(self.clock))
            self.after(1000, self._iterate_counter)

    def _start_counter(self) -> None:
        """
        Kick off the clock from a not running state.
        """
        print("Setting counter running to true")
        self.clock_label.config(text=self.seconds_to_clock(self.clock))
        self.clock_running = True
        self.clock = (
            self.phases[self.phase_index][0] + 1
        )  # Essentially throw away the first time running iterate_counter
        self._iterate_counter()

    def _reset_counter(self) -> None:
        """
        Reset the clock back to the default value in the current phase.
        """
        print("Resetting")
        self.clock = PHASES[self.phase_index][0]
        self.clock_running = False
        self.clock_label.config(text=self.seconds_to_clock(self.clock))
        self.phase_label.config(text=f"PHASE: {self.phases[self.phase_index][1]}")

    def seconds_to_clock(self, seconds: int) -> str:
        """
        Convert a number of seconds into a string representing the minutes and seconds
        in this format -> MM:SS
        """
        current_clock_val = seconds
        mm = current_clock_val // 60
        minutes_str = f"0{mm}" if mm < 10 else str(mm)
        current_clock_val %= 60
        ss = current_clock_val
        seconds_str = f"0{ss}" if ss < 10 else str(ss)
        return f"{minutes_str}:{seconds_str}"


if __name__ == "__main__":
    p = PomodoroTimer(PHASES)
    p.mainloop()
