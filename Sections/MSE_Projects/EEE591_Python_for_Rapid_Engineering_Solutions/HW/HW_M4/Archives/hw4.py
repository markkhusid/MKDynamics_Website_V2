
################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - hw4.py
# Mark Khusid
################################################################################

################################################################################
# Problem: tkinter Based Wealth App with GUI
# Google search: https://www.pythonguis.com/examples/currency-converter-tkinter/
# Google search: https://thepythoncode.com/article/currency-converter-gui-using-tkinter-python
# Google search: https://www.howtogeek.com/make-your-first-graphical-python-app-getting-started-with-tkinter/
################################################################################

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")          # Required for Tkinter compatibility
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants from the assignment
MAX_YEARS = 50
M = 15 # Number of runs

def simulate_wealth(r, sigma, Y, contrib_years, retirement_year, S, N=MAX_YEARS):
    """Simulate ONE Monte Carlo path for N years."""
    noise = (sigma / 100.0) * np.random.randn(N)
    wealth = np.zeros(N + 1)

    for i in range(N):
        growth = 1.0 + (r / 100.0) + noise[i]

        if i < contrib_years:                    # Phase 1: contributing
            wealth[i + 1] = wealth[i] * growth + Y
        elif i < retirement_year:                # Phase 2: growth only
            wealth[i + 1] = wealth[i] * growth 
        else:                                    # Phase 3: retirement - withdraw
            wealth[i + 1] = wealth[i] * growth - S

        if wealth[i + 1] < 0:
            wealth[i + 1] = 0.0

    return wealth


class RetirementGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Retirement Wealth Calculator")
        self.root.geometry("1250x1000")

        style = ttk.Style()
        style.configure("TEntry", font=("Arial", 14))
        style.configure("TLabel", font=("Arial", 14))

        # Variables to store input values
        self.mean_return = tk.DoubleVar(value=6.0)
        self.std_dev = tk.DoubleVar(value=20.0)
        self.yearly_contrib = tk.DoubleVar(value=10000.0)
        self.contrib_years = tk.IntVar(value=30)
        self.retirement_years = tk.IntVar(value=40)
        self.annual_spend = tk.DoubleVar(value=80000.0)

        self.create_widgets()
        self.fig = None
        self.canvas = None

    def create_widgets(self):
        # Frame for inputs
        input_frame = ttk.LabelFrame(self.root, text="Inputs", padding=15)
        input_frame.pack(fill="x", padx=15, pady=10)

        row = 0
        # Mean Return
        ttk.Label(input_frame, text="Mean Return (%)").grid(row=row, column=0, sticky="w", pady=8, padx=5)
        ttk.Entry(input_frame, textvariable=self.mean_return, width=15, style="TEntry").grid(row=row, column=1, pady=8, padx=5)
        row += 1

        # Std Dev Return
        ttk.Label(input_frame, text="Std Dev Return (%)").grid(row=row, column=0, sticky="w", pady=8, padx=5)
        ttk.Entry(input_frame, textvariable=self.std_dev, width=15, style="TEntry").grid(row=row, column=1, pady=8, padx=5)
        row += 1

        # Yearly Contribution
        ttk.Label(input_frame, text="Yearly Contribution ($)").grid(row=row, column=0, sticky="w", pady=8, padx=5)
        ttk.Entry(input_frame, textvariable=self.yearly_contrib, width=15, style="TEntry").grid(row=row, column=1, pady=8, padx=5)
        row += 1

        # No. of Years of Contribution
        ttk.Label(input_frame, text="No. of Years of Contribution").grid(row=row, column=0, sticky="w", pady=8, padx=5)
        ttk.Entry(input_frame, textvariable=self.contrib_years, width=15, style="TEntry").grid(row=row, column=1, pady=8, padx=5)
        row += 1

        # No. of Years to Retirement
        ttk.Label(input_frame, text="No. of Years to Retirement").grid(row=row, column=0, sticky="w", pady=8, padx=5)
        ttk.Entry(input_frame, textvariable=self.retirement_years, width=15, style="TEntry").grid(row=row, column=1, pady=8, padx=5)
        row += 1

        # Annual Spend in Retirement
        ttk.Label(input_frame, text="Annual Retirement Spend ($)").grid(row=row, column=0, sticky="w", pady=8, padx=5)
        ttk.Entry(input_frame, textvariable=self.annual_spend, width=15, style="TEntry").grid(row=row, column=1, pady=8, padx=5)

        # Result label (also larger font)
        self.result_label = ttk.Label(self.root, text="Average Wealth at retirement: $0", 
                                      font=("Arial", 14, "bold"))
        self.result_label.pack(pady=15)

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Calculate", command=self.calculate).grid(row=0, column=0, padx=30)
        ttk.Button(button_frame, text="Quit", command=self.root.quit).grid(row=0, column=1, padx=30)

        # Plot area
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(fill="both", expand=True, padx=15, pady=10)

    def calculate(self):
        r = self.mean_return.get()
        sigma = self.std_dev.get()
        Y = self.yearly_contrib.get()
        contrib_years = self.contrib_years.get()
        retirement_year = self.retirement_years.get()
        S = self.annual_spend.get()

        wealth_paths = []
        retirement_wealths = []

        for _ in range(M):
            path = simulate_wealth(r, sigma, Y, contrib_years, retirement_year, S)
            wealth_paths.append(path)
            retirement_wealths.append(path[retirement_year])

        avg_wealth = np.mean(retirement_wealths)
        self.result_label.config(text=f"Wealth at retirement: ${avg_wealth:,.0f}")

        self.plot_wealth(wealth_paths, retirement_year, contrib_years)

    def plot_wealth(self, wealth_paths, retirement_year, contrib_years):
        
        # Clear old plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(14, 8))
        years = np.arange(len(wealth_paths[0]))

        max_wealth = np.array(wealth_paths).max()
        #print(f"DEBUG: Max wealth across all paths = ${max_wealth:,.0f}")

        colors = plt.cm.tab20(np.linspace(0, 1, len(wealth_paths)))

        for i, path in enumerate(wealth_paths):
            zero_idx = np.where(path[1:] <= 0)[0]

            retirement_value = path[retirement_year]
            final_value = path[-1]

            label = (
                f"Run {i+1}:    "
                f"Ret=\${retirement_value:,.0f},    "
                f"Yr50=\${final_value:,.0f}"
            )
            
            if len(zero_idx) > 0:
                end_idx = zero_idx[0] + 2
                #print(f"[*1] end_idx = {end_idx}")
                #print(f"[*1] zero_idx = {zero_idx}")
                #print(f"[*1] path = {path}")
                ax.plot(
                    years[:end_idx], 
                    path[:end_idx], 
                    color=colors[i], 
                    linewidth=1.5, 
                    alpha=0.5,
                    label=label)
            else:
                #print(f"[*2] zero_idx = {zero_idx}")
                #print(f"[*2] path = {path}")
                #print(path)
                ax.plot(
                    years, 
                    path, 
                    color=colors[i], 
                    linewidth=1.5, 
                    alpha=0.5,
                    label=label)

        # Force correct scaling
        ax.set_ylim(0, max_wealth * 1.08 if max_wealth > 0 else 2_000_000)

        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Wealth ($)", fontsize=12)
        ax.set_title(f"Wealth Over Time — {M} Simulations", fontsize=14)
        ax.grid(True, alpha=0.3)

        ax.axvline(
            x=retirement_year, 
            color='red', 
            linestyle='--', 
            linewidth=2.5, 
            label='Retirement')
        ax.axvline(
            x=contrib_years,
            color='green',
            linestyle='--',
            linewidth=2.0,
            label='End Contributions')
        
        ax.legend(
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            fontsize=8)

        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f'${x:,.0f}'))

        plt.tight_layout()
        fig.subplots_adjust(right=0.70)
        #plt.show(block=False)

        # Embed plot
        self.canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Extra force update for macOS / Tkinter
        #self.canvas.draw_idle()
        #self.root.update_idletasks()
        #self.root.update()

if __name__ == "__main__":
    app = RetirementGUI()
    app.root.mainloop()
