from tkinter import *
from tkinter import ttk
from tkinter import messagebox

PHASES = [
    [5, "WORK"],
    [2, "SHORT REST 1"],
    [5, "WORK"],
    [2, "SHORT REST 2"],
    [5, "WORK"],
    [4, "LONG REST"],
]

phase_index = 0
clock_val = PHASES[phase_index][0]
counter_running = False
root = Tk()
frame = ttk.Frame(root, padding=10)


def seconds_to_clock(seconds):
    current_clock_val = seconds
    mm = current_clock_val // 60
    minutes_str = f"0{mm}" if mm < 10 else str(mm)
    current_clock_val %= 60
    ss = current_clock_val
    seconds_str = f"0{ss}" if ss < 10 else str(ss)
    return f"{minutes_str}:{seconds_str}"


def iterate_counter():
    global clock_val, counter_running, phase_index
    if counter_running:
        print("Counter running is true")
        if clock_val == 0:
            print("Next phase")
            previous_phase = phase_index
            phase_index += 1
            phase_index = phase_index % len(PHASES)
            counter_running = False
            messagebox.showinfo(
                "NEW PHASE!",
                f"{PHASES[previous_phase][1]} has ended.\nPress start to begin new phase, {PHASES[phase_index][1]}",
            )
            reset_counter()
            return
        clock_val -= 1
        lbl.config(text=seconds_to_clock(clock_val))
        root.after(1000, iterate_counter)
    else:
        print("Counter running is false or clock hit zero")


def start_counter():
    print("Setting counter running to true")
    global clock_val, counter_running, phase_index
    lbl.config(text=seconds_to_clock(clock_val))
    counter_running = True
    clock_val = (
        PHASES[phase_index][0] + 1
    )  # Essentially throw away the first time running iterate_counter
    iterate_counter()


def reset_counter():
    global clock_val, counter_running, phase_index
    print("Resetting")
    clock_val = PHASES[phase_index][0]
    counter_running = False
    lbl.config(text=seconds_to_clock(clock_val))
    phase_label.config(text=f"PHASE: {PHASES[phase_index][1]}")


frame.grid()
lbl = ttk.Label(frame, text=seconds_to_clock(clock_val))
phase_label = ttk.Label(frame, text=f"PHASE: {PHASES[phase_index][1]}")
phase_label.grid(column=0, row=0)
lbl.grid(column=0, row=1, pady=(0, 20))
ttk.Button(frame, text="Start", command=start_counter).grid(column=0, row=2, padx=50)
ttk.Button(frame, text="Reset", command=reset_counter).grid(column=0, row=3)
ttk.Button(frame, text="Quit", command=root.destroy).grid(column=0, row=4)
iterate_counter()
root.mainloop()
