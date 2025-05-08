from tkinter import *
from tkinter import ttk, messagebox, PhotoImage

PHASES = [
    [5, "WORK"],
    [2, "SHORT REST 1"],
    [5, "WORK"],
    [2, "SHORT REST 2"],
    [5, "WORK"],
    [4, "LONG REST"],
]


class PomodoroTimer(Tk):
    frame = None
    phases = None
    clock = None
    phase_index = 0
    counter_running = True
    img = None
    clock_label, phase_label, start, reset = None, None, None, None

    def __init__(self, phases: list) -> None:
        super().__init__()
        self.title("Mini Pomodoro")
        self.frame = ttk.Frame(self, padding=10)
        self.frame.grid()
        self.phases = phases
        # for i in range(len(self.phases)):
        #     self.phases[i][0] *= 60
        self.clock = self.phases[self.phase_index][0]
        self.img = PhotoImage(file="tomato.png")
        self.iconphoto(False, self.img)
        ttk.Label(self.frame, image=self.img).grid(column=0, row=0)
        self.clock_label = ttk.Label(self.frame, text=self.seconds_to_clock(self.clock))
        self.phase_label = ttk.Label(
            self.frame, text=f"PHASE: {self.phases[self.phase_index][1]}"
        )
        self.phase_label.grid(column=0, row=1)
        self.clock_label.grid(column=0, row=2, pady=(0, 20))
        ttk.Button(self.frame, text="Start", command=self.start_counter).grid(
            column=0, row=3, padx=50
        )
        ttk.Button(self.frame, text="Reset", command=self.reset_counter).grid(
            column=0, row=4
        )
        ttk.Button(self.frame, text="Quit", command=self.destroy).grid(column=0, row=5)

    def iterate_counter(self):
        if self.counter_running:
            print("Counter running is true")
            if self.clock == 0:
                print("Next phase")
                previous_phase = self.phase_index
                self.phase_index += 1
                self.phase_index %= len(PHASES)
                self.counter_running = False
                messagebox.showinfo(
                    "NEW PHASE!",
                    f"{self.phases[previous_phase][1]} has ended.\nPress start to begin new phase, {self.phases[self.phase_index][1]}",
                )
                self.reset_counter()
                return
            self.clock -= 1
            self.clock_label.config(text=self.seconds_to_clock(self.clock))
            self.after(1000, self.iterate_counter)
        else:
            print("Counter running is false or clock hit zero")

    def start_counter(self):
        print("Setting counter running to true")
        self.clock_label.config(text=self.seconds_to_clock(self.clock))
        self.counter_running = True
        self.clock = (
            self.phases[self.phase_index][0] + 1
        )  # Essentially throw away the first time running iterate_counter
        self.iterate_counter()

    def reset_counter(self):
        print("Resetting")
        self.clock = PHASES[self.phase_index][0]
        self.counter_running = False
        self.clock_label.config(text=self.seconds_to_clock(self.clock))
        self.phase_label.config(text=f"PHASE: {self.phases[self.phase_index][1]}")

    def seconds_to_clock(self, seconds):
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
