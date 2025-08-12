import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import matplotlib
matplotlib.use("TkAgg")  # Set backend BEFORE importing pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulation.simulation import Simulation
import io
import sys
import random


# Redirect stdout to text widget
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
        self.status_var.set("🟢 Ready to simulate")

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

        # Steps Entry
        tk.Label(config_frame, text="Steps:", font=("Helvetica", 11), bg="#161b22", fg="#c9d1d9").pack(side=tk.LEFT, padx=10)
        self.step_entry = tk.Entry(config_frame, font=("Consolas", 11), width=6, bg="#0d1117", fg="#c9d1d9", insertbackground="#c9d1d9")
        self.step_entry.insert(0, "7")
        self.step_entry.pack(side=tk.LEFT)

        # Agents Entry
        tk.Label(config_frame, text="Agents:", font=("Helvetica", 11), bg="#161b22", fg="#c9d1d9").pack(side=tk.LEFT, padx=10)
        self.agent_entry = tk.Entry(config_frame, font=("Consolas", 11), width=6, bg="#0d1117", fg="#c9d1d9", insertbackground="#c9d1d9")
        self.agent_entry.insert(0, "10")
        self.agent_entry.pack(side=tk.LEFT)

        # Tasks Per Step Entry
        tk.Label(config_frame, text="Tasks/Step:", font=("Helvetica", 11), bg="#161b22", fg="#c9d1d9").pack(side=tk.LEFT, padx=10)
        self.task_entry = tk.Entry(config_frame, font=("Consolas", 11), width=6, bg="#0d1117", fg="#c9d1d9", insertbackground="#c9d1d9")
        self.task_entry.insert(0, "3")
        self.task_entry.pack(side=tk.LEFT)

        # Dropouts Per Step Entry
        tk.Label(config_frame, text="Dropouts/Step:", font=("Helvetica", 11), bg="#161b22", fg="#c9d1d9").pack(side=tk.LEFT, padx=10)
        self.dropout_entry = tk.Entry(config_frame, font=("Consolas", 11), width=6, bg="#0d1117", fg="#c9d1d9", insertbackground="#c9d1d9")
        self.dropout_entry.insert(0, "2")
        self.dropout_entry.pack(side=tk.LEFT)

        # Run Button
        tk.Button(config_frame, text="▶ Run", font=("Helvetica", 11, "bold"), bg="#238636", fg="white",
                  command=self.run_simulation).pack(side=tk.LEFT, padx=15)

        # Save Logs Button
        tk.Button(config_frame, text="💾 Save Logs", font=("Helvetica", 10), command=self.save_logs,
                  bg="#2d333b", fg="white").pack(side=tk.RIGHT, padx=10)

        # Output Text Area
        self.output_text = scrolledtext.ScrolledText(self.log_tab, wrap=tk.WORD, font=("Courier New", 11),
                                                     bg="#010409", fg="#3fb950", insertbackground="white")
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.output_text.config(state=tk.DISABLED)

    def build_graph_tab(self):
        # 3 subplot layout
        self.figure, (self.ax_harmony, self.ax_rq, self.ax_ro) = plt.subplots(
            3, 1, figsize=(10, 8), dpi=100, facecolor='#0d1117'
        )

        for ax in (self.ax_harmony, self.ax_rq, self.ax_ro):
            ax.set_facecolor("#161b22")
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')

        self.ax_harmony.set_title("Harmony Index", color="white")
        self.ax_rq.set_title("RQ", color="white")
        self.ax_ro.set_title("Reassignment Overhead (RO)", color="white")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(self.graph_tab, bg="#0d1117")
        btn_frame.pack()

        tk.Button(btn_frame, text="💾 Save Graph", command=self.save_graph,
                  bg="#238636", fg="white", font=("Helvetica", 10)).pack(pady=5)

    def build_viz_tab(self):
        self.canvas_viz = tk.Canvas(self.viz_tab, width=self.canvas_size, height=self.canvas_size, bg="#0d1117", highlightthickness=0)
        self.canvas_viz.pack(padx=20, pady=20)

        tk.Button(self.viz_tab, text="🦎 Launch NetLogo", font=("Helvetica", 11),
                  command=self.launch_netlogo_viz, bg="#238636", fg="white").pack(pady=10)

    def redirect_stdout(self):
        sys.stdout = RedirectText(self.output_text)

    def run_simulation(self):
        # Clear previous output
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)

        try:
            steps = int(self.step_entry.get())
            agents = int(self.agent_entry.get())
            tasks_per_step = int(self.task_entry.get())
            dropouts_per_step = int(self.dropout_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "All fields must be integers.")
            return

        self.status_var.set("⏳ Running simulation...")
        self.root.update_idletasks()

        sys.stdout = RedirectText(self.output_text)
        self.output_text.config(state=tk.NORMAL)

        sim = Simulation(
            agent_count=agents,
            tasks_per_step=tasks_per_step,
            dropouts_per_step=dropouts_per_step
        )

        sim.run(steps=steps)

        # Get histories
        harmony_history = getattr(sim, "harmony_history", [])
        rq_history = getattr(sim, "rq_history", [])
        ro_history = getattr(sim, "ro_history", [])

        # Update graphs
        self.update_graphs(harmony_history, rq_history, ro_history)

        sys.stdout = sys.__stdout__
        self.output_text.config(state=tk.DISABLED)

        self.animate_agents(steps, agents)
        self.status_var.set("✅ Simulation completed successfully.")

    def update_graphs(self, harmony, rq, ro):
        self.ax_harmony.clear()
        self.ax_rq.clear()
        self.ax_ro.clear()

        self.ax_harmony.plot(harmony, color="cyan")
        self.ax_harmony.set_title("Harmony Index", color="white")

        self.ax_rq.plot(rq, color="orange")
        self.ax_rq.set_title("RQ", color="white")

        self.ax_ro.plot(ro, color="magenta")
        self.ax_ro.set_title("Reassignment Overhead (RO)", color="white")

        for ax in (self.ax_harmony, self.ax_rq, self.ax_ro):
            ax.set_facecolor("#161b22")
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')

        self.canvas.draw()

    def animate_agents(self, steps, agents):
        self.canvas_viz.delete("all")
        width, height = self.canvas_size, self.canvas_size

        positions = [(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(agents)]
        tasks = [(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(agents//2)]

        agent_objs = []
        for x, y in positions:
            circle = self.canvas_viz.create_oval(x-10, y-10, x+10, y+10, fill="#58a6ff", outline="")
            agent_objs.append((circle, x, y))

        for x, y in tasks:
            self.canvas_viz.create_rectangle(x-5, y-5, x+5, y+5, fill="#f9c74f", outline="")

        def move_step(step):
            if step >= steps:
                return
            for i, (circle, x, y) in enumerate(agent_objs):
                tx, ty = tasks[i % len(tasks)]
                new_x = x + (tx - x) * 0.2
                new_y = y + (ty - y) * 0.2
                self.canvas_viz.move(circle, new_x - x, new_y - y)
                agent_objs[i] = (circle, new_x, new_y)
            self.root.after(500, lambda: move_step(step + 1))

        move_step(0)

    def launch_netlogo_viz(self):
        try:
            from netlogo_integration import NetLogoVisualizer
            agents = [{"name": f"C{i+1}", "role": "Contributor"} for i in range(int(self.agent_entry.get()))]
            visualizer = NetLogoVisualizer(agent_data=agents)
            visualizer.setup_agents()
            visualizer.run_steps(10)
            visualizer.close()
            self.status_var.set("🦎 NetLogo visualization completed")
        except Exception as e:
            messagebox.showerror("NetLogo Error", str(e))
            self.status_var.set("❌ NetLogo failed")

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
