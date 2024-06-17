import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def create_plot(step):
    plt.clf()
    current_df = df[df['step'] == step]
    plt.scatter(current_df['x'], current_df['y'])
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.title(f"Step: {step}")

def main():
    num_steps = 100
    df = pd.read_csv("data.csv")
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, create_plot, frames=range(num_steps), repeat=False)


if __name__ == "__main__":
    main()