import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from simulation.simulation import Simulation
import io
import sys

def run_simulation():
    try:
        steps = int(step_entry.get())
        agents = int(agent_entry.get())

        sim = Simulation(agent_count=agents)  # Pass dynamic agent count here

        buffer = io.StringIO()
        sys.stdout = buffer

        sim.run(steps=steps)

        sys.stdout = sys.__stdout__

        output = buffer.getvalue()
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output.strip())
        output_text.config(state=tk.DISABLED)

    except ValueError:
        sys.stdout = sys.__stdout__
        messagebox.showerror("Invalid Input", "Please enter valid numbers for steps and agents.")
    except Exception as e:
        sys.stdout = sys.__stdout__
        messagebox.showerror("Error", str(e))

def clear_logs():
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)

def save_logs():
    log = output_text.get(1.0, tk.END).strip()
    if not log:
        messagebox.showinfo("Nothing to Save", "Simulation log is empty.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(log)
        messagebox.showinfo("Saved", f"Logs saved to {file_path}")

# ----------------------
# GUI Setup
# ----------------------
root = tk.Tk()
root.title("🌱 SustainHub Simulation")
root.geometry("950x720")
root.resizable(False, False)
root.configure(bg="#eaf4f4")

# Title
title = tk.Label(root, text="🌱 SustainHub Simulation Tool", font=("Helvetica", 22, "bold"), bg="#eaf4f4", fg="#2e4053")
title.pack(pady=20)

# ----------------------
# Input Frame
# ----------------------
input_frame = tk.Frame(root, bg="#eaf4f4")
input_frame.pack(pady=10)

# Steps input
tk.Label(input_frame, text="Steps:", font=("Helvetica", 12), bg="#eaf4f4").grid(row=0, column=0, padx=10)
step_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=6, justify="center")
step_entry.insert(0, "7")
step_entry.grid(row=0, column=1)

# Agents input
tk.Label(input_frame, text="Agents:", font=("Helvetica", 12), bg="#eaf4f4").grid(row=0, column=2, padx=10)
agent_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=6, justify="center")
agent_entry.insert(0, "10")
agent_entry.grid(row=0, column=3)

# Run button
run_button = tk.Button(input_frame, text="▶ Run", font=("Helvetica", 12, "bold"),
                       bg="#3498db", fg="white", padx=15, pady=5, command=run_simulation)
run_button.grid(row=0, column=4, padx=20)

# ----------------------
# Action Buttons
# ----------------------
button_frame = tk.Frame(root, bg="#eaf4f4")
button_frame.pack(pady=5)

clear_button = tk.Button(button_frame, text="🧹 Clear Logs", font=("Helvetica", 11), command=clear_logs,
                         bg="#f39c12", fg="white", padx=15, pady=4)
clear_button.pack(side=tk.LEFT, padx=10)

save_button = tk.Button(button_frame, text="💾 Save Logs", font=("Helvetica", 11), command=save_logs,
                        bg="#27ae60", fg="white", padx=15, pady=4)
save_button.pack(side=tk.LEFT, padx=10)

# ----------------------
# Output Frame
# ----------------------
output_frame = tk.Frame(root, bg="#eaf4f4")
output_frame.pack(pady=10, fill=tk.BOTH, expand=True)

output_label = tk.Label(output_frame, text="📜 Simulation Output Log", font=("Helvetica", 15, "bold"), bg="#eaf4f4", fg="#1c2833")
output_label.pack(anchor="w", padx=12)

output_text = scrolledtext.ScrolledText(
    output_frame,
    wrap=tk.WORD,
    width=115,
    height=25,
    font=("Courier New", 10),
    bg="#fdfefe",
    bd=2,
    relief=tk.SUNKEN
)
output_text.pack(padx=12, fill=tk.BOTH, expand=True)
output_text.config(state=tk.DISABLED)

# Footer
footer = tk.Label(root, text="Built for Open Source Community Simulation", font=("Helvetica", 9), bg="#eaf4f4", fg="#7b8a8b")
footer.pack(pady=10)

root.mainloop()
