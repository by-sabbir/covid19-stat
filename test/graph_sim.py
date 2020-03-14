import numpy as np
import matplotlib.pyplot as plt


class CreateSin():
    
    def __init__(self, x, y):
        self.x = x
        self.y = np.sin(x)

    def sin_graph(self):
        self.x = np.linspace(-360, 360, 10)
        y = np.sin(x)
        plt.plot(x, y)
        return x, y

    

if __name__ == "__main__":
    main()
    