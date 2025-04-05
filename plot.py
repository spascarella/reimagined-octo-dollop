import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from config import COLOR, SYMBOLS

def plot_grid_from_file(grid, title="Predicted Output"):
    grid_np = np.array(grid)

    if grid_np.shape[0] < 30 or grid_np.shape[1] < 30:
        padded_grid = np.zeros((30, 30), dtype=int)
        h, w = grid_np.shape
        padded_grid[:h, :w] = grid_np
        grid_np = padded_grid

    cmap = ListedColormap(COLOR)
    plt.figure(figsize=(6, 6))
    plt.imshow(grid_np, cmap=cmap, vmin=0, vmax=9)
    plt.title(title)
    plt.axis("off")
    plt.show()

def print_predicted_grid(grid):
    for row in grid:
        print(' '.join(SYMBOLS.get(cell, str(cell)) for cell in row))

def check_and_plot(predicted, ground_truth):
    pred_np = np.array(predicted)
    true_np = np.array(ground_truth)
    h, w = true_np.shape
    pred_cropped = pred_np[:h, :w]

    if np.array_equal(pred_cropped, true_np):
        print("The predicted output matches the true output")
    else:
        print("The predicted output does not match the true output")

    print_predicted_grid(pred_cropped.tolist())
    plot_grid_from_file(pred_cropped.tolist(), title="Predicted Output Grid")