import tkinter as tk
from tkinter import messagebox, scrolledtext
from simulation.simulation import Simulation
import io
import sys

def run_simulation():
    try:
        steps = int(step_entry.get())
        sim = Simulation()

        # Capture printed output
        buffer = io.StringIO()
        sys.stdout = buffer

        sim.run(steps=steps)

        sys.stdout = sys.__stdout__  # Reset stdout

        output = buffer.getvalue()
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output.strip())
        output_text.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for steps.")
    except Exception as e:
        sys.stdout = sys.__stdout__
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("SustainHub Simulation")
root.geometry("820x620")
root.resizable(False, False)
root.configure(bg="#f7f7f7")

# Title label
title = tk.Label(root, text="🌱 SustainHub Simulation", font=("Helvetica", 20, "bold"), bg="#f7f7f7", fg="#333")
title.pack(pady=20)

# Frame for step input and run button
input_frame = tk.Frame(root, bg="#f7f7f7")
input_frame.pack(pady=10)

step_label = tk.Label(input_frame, text="Steps:", font=("Helvetica", 12), bg="#f7f7f7")
step_label.pack(side=tk.LEFT, padx=(0, 10))

step_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=5, justify="center")
step_entry.insert(0, "7")
step_entry.pack(side=tk.LEFT, padx=(0, 10))

run_button = tk.Button(input_frame, text="▶ Run Simulation", font=("Helvetica", 12, "bold"),
                       bg="#4CAF50", fg="white", padx=10, pady=5, command=run_simulation)
run_button.pack(side=tk.LEFT)

# Log output (non-editable)
output_frame = tk.Frame(root, bg="#f7f7f7")
output_frame.pack(pady=15)

output_label = tk.Label(output_frame, text="Simulation Log:", font=("Helvetica", 14, "bold"), bg="#f7f7f7")
output_label.pack(anchor="w", padx=10)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=100, height=25, font=("Courier", 10), bg="#ffffff")
output_text.pack(padx=10)
output_text.config(state=tk.DISABLED)  # Make it read-only

root.mainloop()
