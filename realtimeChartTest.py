# -*- coding: utf8 -*-
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation


def main():

    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    x = []
    y = []

    for i in range(100):
        x.append(i)
        y.append(0)
        if i == 99:
            y[i] = random.randint(5, 95)

    # Create an empty line object
    line, = ax.plot([], [])

    # Update function to update the line data
    def update(i):

        for i in range(100):
            if i == 99:
                y[i] = random.randint(5, 95)
            else:
                y[i] = y[i+1]



        line.set_data(x, y)
        ax.relim()
        ax.autoscale_view()

        return line,

    # Animate the chart
    ani = matplotlib.animation.FuncAnimation(fig, update, frames=1000, interval=100, blit=True)

    # Show the chart
    plt.show()

if __name__ == "__main__":
    main()
