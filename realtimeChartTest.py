# -*- coding: utf8 -*-
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import numpy as np

def main():

    fig, ax = plt.subplots()

    x = np.linspace(0, 360, num=60)
    y = np.sin(x)

    def update(frame):
        """
        - frames에 따라서 매번 업데이트로 그림을 그려줌.
        - frame은 FuncAnimation의 frame argument에 있는 값이 넘어가는 부분.
        """
        ax.clear() # 일단 지금 그려진 부분을 다 지우고,

        ax.set_xlim(0,360)
        ax.set_ylim(-1.5,1.5)
        ax.grid(True)

        # 여기서처럼 그림을 새로 그려주면 됨.
        plt.plot(x[:frame], y[:frame])
    """
    - 아래 argument에서 blit가 False인 것이 중요합니다. 
    - True일 경우에는 update function에서 artist object를 넘겨줘야 합니다. 예를 들면 Line 같은 것들. 
    """


    ani = FuncAnimation(
        fig=fig,
        func=update,
        frames=60,
        interval=100,
        blit=False,
    )

    # Show the chart
    plt.show()

if __name__ == "__main__":
    main()


"""
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
    line, = ax.plot(x, y, 'b-')

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
"""