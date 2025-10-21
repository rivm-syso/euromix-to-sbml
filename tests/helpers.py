import math
import pandas as pd
import matplotlib.pyplot as plt

def generateBolusDoseEventsPattern(amount, start, step, stop):
    """ Helper function for generating bolus dosing event patterns """
    timings = range(start, stop, step)
    events = []
    for timing in timings:
        events.append((timing, amount))
    return events

def generateContinuousDoseEventsPattern(amount, duration, start, step, stop):
    """ Helper function for generating continuous dosing event patterns """
    timings = range(start, stop, step)
    events = []
    for timing in timings:
        events.append((timing, amount, duration))
    return events

# Helper function for loading parametrisations
def load_parametrisation(model, filename, idInstance):
    df = pd.read_csv(filename)
    df['Value'] = df['Value'].astype(float)
    df = df.loc[df['idModelInstance'] == idInstance]
    for index, row in df.iterrows():
        model[str(row['Parameter'])] = row['Value']

# Helper function for plotting simulation results
def plot_simulation_results(res, selections, ncols=4):
    nrows = math.ceil((len(selections) - 1)/ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(3*ncols, 3*nrows))
    axes = axes.flatten()
    for ax in axes:
        ax.set(xlabel='time') 
    labels = selections
    for i in range(1, len(selections)):
        sid = selections[i]
        axes[i-1].plot(res['time'], res[sid], linewidth=1)
        axes[i-1].set(ylabel=labels[i])
    for j in range(len(selections), nrows*ncols + 1):
        fig.delaxes(axes[j-1])
    fig.tight_layout()
    return fig
