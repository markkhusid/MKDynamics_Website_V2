################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - hw4.py
# Mark Khusid
################################################################################

################################################################################
# Problem: tkinter Based Wealth App with GUI
# Google search: https://www.pythonguis.com/examples/currency-converter-tkinter/
# Google search: https://thepythoncode.com/article/currency-converter-gui-using-tkinter-python
# Google search: https://www.howtogeek.com/make-your-first-graphical-python-app-getting-started-with-tkinter/
# Additional AI assistance provided by Github Copilot and Microsoft Visual Studio Code IntelliSense
# All comments are provided by Github Copilot and Microsoft Visual Studio Code IntelliSense, with some edits by the author for clarity and formatting.
################################################################################

# This code implements a tkinter-based GUI application to simulate retirement wealth.
import tkinter as tk
from tkinter import ttk
import numpy as np

# Matplotlib imports for plotting
import matplotlib
matplotlib.use("TkAgg")          # Required for Tkinter compatibility
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants from the assignment
MAX_YEARS = 50 # Total years to simulate (30 years contribution + 20 years retirement)
M = 15 # Number of runs

# Define the simulate_wealth function
#################################################################################################
# Simulate the wealth over time based on the given parameters.                                  #
# This function will be called for each Monte Carlo run                                         #
# to generate a wealth path.                                                                    # 
#                                                                                               #
# input:                                                                                        #
#    r: mean return (%)                                                                         #
#    sigma: standard deviation of returns (%)                                                   #
#    Y: yearly contribution ($)                                                                 #
#    contrib_years: number of years contributing to the retirement fund (e.g., 30)              #
#    retirement_year: number of years until retirement (e.g., 30)                               #
#    S: annual spend in retirement ($)                                                          #
#    N: total number of years to simulate (default is MAX_YEARS, which is 50)                   #
# output:                                                                                       #
#    returns an array of wealth values for each year, including the initial year (year 0)       #
#################################################################################################
def simulate_wealth(r, sigma, Y, contrib_years, retirement_year, S, N=MAX_YEARS):
    # Simulate one path for N years.

    # Generate random returns for each year based on the mean and standard deviation
    noise = (sigma / 100.0) * np.random.randn(N)

    # Initialize wealth array to store the wealth at each year, starting with 0 at year 0
    wealth = np.zeros(N + 1)

    # Simulate the wealth over time based on the growth and contributions/withdrawals
    for i in range(N):
        # Calculate the growth factor for the year based on the mean return, random noise, and convert percentage to a multiplier
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

# Define the RetirementGUI class to create the GUI application
class RetirementGUI:
    # Constructor to initialize the GUI application
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        # Set the title and size of the window
        self.root.title("Retirement Wealth Calculator")
        self.root.geometry("1250x1000")

        # Configure the style for the widgets
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

        # Create the widgets for the GUI
        self.create_widgets()
        self.fig = None
        self.canvas = None

    # Method to create the widgets for the GUI
    #################################################################################################
    # Create widgets method of class RetirementGUI                                                  #
    # This method creates the input fields, buttons, and plot area for the GUI application.         #
    # to generate a wealth path.                                                                    # 
    #                                                                                               #
    # input:                                                                                        #
    #    None (this method uses the instance variables for input values)                            #
    # output:                                                                                       #
    #    None (this method creates and places the widgets in the GUI)                               #
    #################################################################################################
    def create_widgets(self):
        # Frame for inputs
        input_frame = ttk.LabelFrame(self.root, text="Inputs", padding=15)
        input_frame.pack(fill="x", padx=15, pady=10)

        # Initialize row counter for grid placement
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

    # Method to perform the calculation and update the results and plot
    #################################################################################################
    # Calculate method of class RetirementGUI                                                       #
    # This method gets the input values from the GUI and performs the retirement calculations.      #
    # It then updates the result label with the average wealth at retirement                        #
    # and calls the plot method                                                                     #
    #                                                                                               #
    # input:                                                                                        #
    #    None (this method uses the instance variables for input values)                            #
    # output:                                                                                       #
    #    None (this method updates the GUI with the calculation results)                             #
    #################################################################################################
    def calculate(self):
        # Retrieve input values from the GUI
        r = self.mean_return.get()
        sigma = self.std_dev.get()
        Y = self.yearly_contrib.get()
        contrib_years = self.contrib_years.get()
        retirement_year = self.retirement_years.get()
        S = self.annual_spend.get()

        # Initialize lists to store wealth paths and retirement wealths for each simulation run
        wealth_paths = []
        retirement_wealths = []

        # Run the simulations M times and store the results
        for _ in range(M):
            path = simulate_wealth(r, sigma, Y, contrib_years, retirement_year, S)
            wealth_paths.append(path)
            retirement_wealths.append(path[retirement_year])

        # Calculate the average wealth at retirement and update the result label
        avg_wealth = np.mean(retirement_wealths)
        self.result_label.config(text=f"Wealth at retirement: ${avg_wealth:,.0f}")

        # 
        self.plot_wealth(wealth_paths, retirement_year, contrib_years)

    # Method to plot the wealth paths for each simulation run
    #######################################################################################################
    # Plot wealth method of class RetirementGUI                                                           #
    # This method takes the wealth paths generated from the simulations and plots them using Matplotlib.  #
    # It also adds vertical lines to indicate the retirement year and the end of contributions.           #
    #                                                                                                     #
    # input:                                                                                              #
    #    wealth_paths: a list of arrays, where each array contains the wealth values                      #
    #                  for each year of a simulation run.                                                 #
    #    retirement_year: the year at which retirement occurs (used to plot the vertical line)            #
    #    contrib_years: the number of years of contribution (used to plot the vertical line)              #
    # output:                                                                                             #
    #    None (this method updates the plot area in the GUI with the new plot of wealth paths)            #
    ####################################################################################################### 
    def plot_wealth(self, wealth_paths, retirement_year, contrib_years):
        
        # Clear old plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Create the plot 
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Generate an array of years for the x-axis based on the length of the wealth paths (which should all be the same length)
        years = np.arange(len(wealth_paths[0]))

        # Determine the maximum wealth across all paths to set the y-axis limit appropriately
        max_wealth = np.array(wealth_paths).max()
        #print(f"DEBUG: Max wealth across all paths = ${max_wealth:,.0f}")

        # Generate a color map for the lines to ensure they are visually distinct
        colors = plt.cm.tab20(np.linspace(0, 1, len(wealth_paths)))

        # Loop through each wealth path and plot it, adding labels for the retirement value and final value.        
        for i, path in enumerate(wealth_paths):
            # Find the index where wealth first drops to zero or below (if it happens) to stop the plot at that point
            zero_idx = np.where(path[1:] <= 0)[0]

            # Get the wealth value at retirement and the final wealth value for labeling
            retirement_value = path[retirement_year]
            # Get the final wealth value at the end of the simulation (year 50)
            final_value = path[-1]

            # Create a label for the line that includes the retirement value and final value, formatted with commas and dollar signs for readability
            label = (
                f"Run {i+1}:    "
                f"Ret=\${retirement_value:,.0f},    "
                f"Yr50=\${final_value:,.0f}"
            )
            
            # If the wealth drops to zero at some point, we only plot up to that point to avoid plotting negative wealth values. Otherwise, we plot the entire path.
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
            # else, we plot the entire run
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

        # Label the horizontal axis with the time dimension in years
        ax.set_xlabel("Year", fontsize=12)
        # Label the vertical axis with the simulated wealth values in dollars
        ax.set_ylabel("Wealth ($)", fontsize=12)
        # Add a descriptive title showing the wealth trajectory and number of simulations
        ax.set_title(f"Wealth Over Time — {M} Simulations", fontsize=14)
        ax.grid(True, alpha=0.3)

        # Draw a vertical dashed line at the retirement year to mark the retirement transition
        ax.axvline(
            x=retirement_year, 
            color='red', 
            linestyle='--', 
            linewidth=2.5, 
            label='Retirement')
        
        # Draw a vertical dashed line at the last contribution year to show when savings contributions stop
        ax.axvline(
            x=contrib_years,
            color='green',
            linestyle='--',
            linewidth=2.0,
            label='End Contributions')
        
        # Place the legend outside the plot area so the plotted lines remain visible
        ax.legend(
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            fontsize=8)

        # Format y-axis labels as dollar amounts with commas and no decimals
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f'${x:,.0f}'))

        # Adjust layout to prevent overlapping elements and make room for the legend
        plt.tight_layout()
        fig.subplots_adjust(right=0.70)

        # Embed the Matplotlib figure into the Tkinter frame and render it
        self.canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

   
if __name__ == "__main__":
    # Intiatiate the class
    app = RetirementGUI()
    # Run the app!
    app.root.mainloop()
