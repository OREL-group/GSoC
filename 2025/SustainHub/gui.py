import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from simulation.simulation import Simulation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
import sys
import random

# Redirect stdout to text widget....
class RedirectText(io.StringIO):
    def __init__(self, text_area):
        super().__init__()
        self.text_area = text_area

    def write(self, string):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, string)
        self.text_area.see(tk.END)
        self.text_area.configure(state='disabled')

    def flush(self):
        pass

class SustainHubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SustainHub Simulation — GitHub Style")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0d1117")

        self.agent_widgets = []
        self.task_widgets = []
        self.canvas_size = 600
        self.agent_radius = 10

        self.build_ui()

    def build_ui(self):
        self.status_var = tk.StringVar()
        self.status_var.set(" Ready to simulate")

        self.build_header()
        self.build_tabs()
        self.redirect_stdout()

    def build_header(self):
        header = tk.Frame(self.root, bg="#161b22")
        header.pack(fill=tk.X)

        tk.Label(header, text="SustainHub Simulation", font=("Helvetica", 22, "bold"),
                 bg="#161b22", fg="#c9d1d9").pack(side=tk.LEFT, padx=20, pady=10)

        footer = tk.Label(self.root, text="Powered by SustainHub • GitHub Themed UI • GSoC 2025",
                         font=("Helvetica", 9), bg="#0d1117", fg="#6e7681")
        footer.pack(side=tk.BOTTOM, pady=5)

        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.FLAT, anchor=tk.W,
                              bg="#161b22", fg="#c9d1d9", font=("Helvetica", 10))
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def build_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', background="#161b22", foreground="#c9d1d9", font=("Helvetica", 10))
        style.map("TNotebook.Tab", background=[("selected", "#238636")])

        self.log_tab = tk.Frame(notebook, bg="#0d1117")
        self.graph_tab = tk.Frame(notebook, bg="#0d1117")
        self.viz_tab = tk.Frame(notebook, bg="#0d1117")

        notebook.add(self.log_tab, text="📝 Logs")
        notebook.add(self.graph_tab, text="📊 Graphs")
        notebook.add(self.viz_tab, text="🎯 Visualizer")

        self.build_log_tab()
        self.build_graph_tab()
        self.build_viz_tab()

    def build_log_tab(self):
        config_frame = tk.Frame(self.log_tab, bg="#161b22")
        config_frame.pack(fill=tk.X, pady=10, padx=10)

        tk.Label(config_frame, text="Steps:", font=("Helvetica", 11), bg="#161b22", fg="#c9d1d9").pack(side=tk.LEFT, padx=10)
        self.step_entry = tk.Entry(config_frame, font=("Consolas", 11), width=6, bg="#0d1117", fg="#c9d1d9",
                                   insertbackground="#c9d1d9")
        self.step_entry.insert(0, "7")
        self.step_entry.pack(side=tk.LEFT)

        tk.Label(config_frame, text="Agents:", font=("Helvetica", 11), bg="#161b22", fg="#c9d1d9").pack(side=tk.LEFT, padx=10)
        self.agent_entry = tk.Entry(config_frame, font=("Consolas", 11), width=6, bg="#0d1117", fg="#c9d1d9",
                                    insertbackground="#c9d1d9")
        self.agent_entry.insert(0, "10")
        self.agent_entry.pack(side=tk.LEFT)

        tk.Button(config_frame, text="▶ Run", font=("Helvetica", 11, "bold"), bg="#238636", fg="red",
                  command=self.run_simulation).pack(side=tk.LEFT, padx=15)

        tk.Button(config_frame, text="💾 Save Logs", font=("Helvetica", 10), command=self.save_logs,
                  bg="#2d333b", fg="red").pack(side=tk.RIGHT, padx=10)

        self.output_text = scrolledtext.ScrolledText(self.log_tab, wrap=tk.WORD, font=("Courier New", 11),
                                                     bg="#010409", fg="#3fb950", insertbackground="white")
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.output_text.config(state=tk.DISABLED)

    def build_graph_tab(self):
        self.figure = plt.Figure(figsize=(10, 5), dpi=100, facecolor='#0d1117')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Simulation Graph", color="white")
        self.ax.set_facecolor("#161b22")
        self.ax.tick_params(colors='white')
        self.ax.spines[:].set_color('white')

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(self.graph_tab, bg="#0d1117")
        btn_frame.pack()

        tk.Button(btn_frame, text="💾 Save Graph", command=self.save_graph,
                  bg="#238636", fg="white", font=("Helvetica", 10)).pack(pady=5)

    def build_viz_tab(self):
        self.canvas = tk.Canvas(self.viz_tab, width=self.canvas_size, height=self.canvas_size, bg="#0d1117", highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)

    def redirect_stdout(self):
        sys.stdout = RedirectText(self.output_text)

    def run_simulation(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)

        try:
            steps = int(self.step_entry.get())
            agents = int(self.agent_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Steps and Agents must be integers.")
            return

        self.status_var.set("⏳ Running simulation...")
        self.root.update_idletasks()

        sim = Simulation(agent_count=agents)
        result = sim.run(steps=steps)

        if result:
            self.plot_graph(result)
            self.animate_agents(steps, agents)
            self.status_var.set("✅ Simulation completed successfully.")
        else:
            self.status_var.set("⚠️ Simulation returned no data.")

    def plot_graph(self, result):
        self.ax.clear()
        self.ax.set_title("Agent Reward over Steps", color="white")
        self.ax.set_facecolor("#161b22")
        self.ax.tick_params(colors='white')
        self.ax.spines[:].set_color('white')

        self.ax.plot(result["steps"], result["rewards"], marker='o', color="#58a6ff", label="Reward")
        self.ax.set_xlabel("Steps", color="white")
        self.ax.set_ylabel("Reward", color="white")
        self.ax.legend(facecolor="#0d1117", edgecolor="white", labelcolor="white")
        self.canvas.draw()

    def animate_agents(self, steps, agents):
        self.canvas.delete("all")
        width, height = self.canvas_size, self.canvas_size

        positions = [(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(agents)]
        tasks = [(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(agents//2)]

        agent_objs = []
        for x, y in positions:
            circle = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="#58a6ff", outline="")
            agent_objs.append((circle, x, y))

        for x, y in tasks:
            self.canvas.create_rectangle(x-5, y-5, x+5, y+5, fill="#f9c74f", outline="")

        def move_step(step):
            if step >= steps:
                return

            for i, (circle, x, y) in enumerate(agent_objs):
                tx, ty = tasks[i % len(tasks)]
                new_x = x + (tx - x) * 0.2
                new_y = y + (ty - y) * 0.2
                self.canvas.move(circle, new_x - x, new_y - y)
                agent_objs[i] = (circle, new_x, new_y)

            self.root.after(500, lambda: move_step(step + 1))

        move_step(0)

    def save_logs(self):
        content = self.output_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showinfo("Nothing to Save", "Log is empty.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, 'w') as f:
                f.write(content)
            self.status_var.set("📁 Logs saved")

    def save_graph(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if path:
            self.figure.savefig(path, facecolor='#0d1117')
            self.status_var.set("📈 Graph saved")

if __name__ == "__main__":
    root = tk.Tk()
    app = SustainHubApp(root)
    root.mainloop()
