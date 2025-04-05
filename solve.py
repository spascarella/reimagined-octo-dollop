import json
from collections import deque
import copy
from plot import check_and_plot
from config import MIN_COMPONENT_SIZE

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def find_components(grid):
    """Find all connected components in a grid through DFS"""
    rows, columns = len(grid), len(grid[0])
    visited = [[False for _ in range(columns)] for _ in range(rows)]
    components = []

    def dfs(i, j, current_component):
        if i < 0 or i >= rows or j < 0 or j >= columns:
            return
        if visited[i][j] or grid[i][j] != 1:
            return
        
        visited[i][j] = True
        current_component.append((i, j))
        
        for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
            dfs(i+di, j+dj, current_component)

    for i in range(rows):
        for j in range(columns):
            if grid[i][j] == 1 and not visited[i][j]:
                component = []
                dfs(i, j, component)
                components.append(component)
    return components

def get_bounding_box(component):
    """Get the bounding box of a component"""
    rows = [i for i, _ in component]
    columns = [j for _, j in component]
    return min(rows), max(rows), min(columns), max(columns)

def extract_subgrid(grid, bbox):
    """Extract the subgrid defined by the bounding box"""
    min_i, max_i, min_j, max_j = bbox
    return [row[min_j:max_j+1] for row in grid[min_i:max_i+1]]

def flood_fill_zeros(subgrid):
    """Flood fill to find all zeros in the subgrid"""
    h, w = len(subgrid), len(subgrid[0])
    visited = [[False]*w for _ in range(h)]
    q = deque()

    for i in range(h):
        for j in range(w):
            if (i == 0 or j == 0 or i == h-1 or j == w-1) and subgrid[i][j] == 0:
                q.append((i, j))
                visited[i][j] = True
    while q:
        i, j = q.popleft()
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < h and 0 <= nj < w and not visited[ni][nj] and subgrid[ni][nj] == 0:
                visited[ni][nj] = True
                q.append((ni, nj))
    return visited

def is_closed_shape(grid, component):
    """Check if a component is a closed shape"""
    bbox = get_bounding_box(component)
    subgrid = extract_subgrid(grid, bbox)
    visited = flood_fill_zeros(subgrid)

    for i in range(len(subgrid)):
        for j in range(len(subgrid[0])):
            if subgrid[i][j] == 0 and not visited[i][j]:
                return True
    return False

def fill_inner_area(grid, output_grid, component):
    """Fill the first inner layer of a component with green squares"""
    min_i, max_i, min_j, max_j = get_bounding_box(component)
    subgrid = extract_subgrid(grid, (min_i, max_i, min_j, max_j))
    visited = flood_fill_zeros(subgrid)

    for i in range(1, len(subgrid) - 1):
        for j in range(1, len(subgrid[0]) - 1):
            if subgrid[i][j] == 0 and not visited[i][j]:
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                    ni, nj = i + di, j + dj
                    if subgrid[ni][nj] == 1:
                        output_grid[min_i + i][min_j + j] = 3
                        break
                    
def fill_outer_area(grid, output_grid, component):
    """Fill the first outer layer area of a component with red squares"""
    for i, j in component:
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                if grid[ni][nj] == 0 and output_grid[ni][nj] == 0:
                    output_grid[ni][nj] = 2

def save_grid(grid, path):
    final_grid = []
    for row in grid:
        new_row = []
        for val in row:
            if val == '.':
                new_row.append(0)
            elif val == '#':
                new_row.append(1)
            else:
                new_row.append(int(val))
        final_grid.append(new_row)
    with open(path, 'w') as f:
        json.dump(final_grid, f, indent=2)
    print(f"Grid saved to {path}")


def solve():
    input_file = "./input/d931c21c.json"
    output_path = "./output/"
    data = read_json(input_file)
    true_output = data["test"][0]["output"]
    
    data = data["test"][0]["input"]
    output_grid = copy.deepcopy(data)

    components = find_components(data)
    filtered = [c for c in components if len(c) >= MIN_COMPONENT_SIZE]

    for idx, comp in enumerate(filtered):
      if is_closed_shape(data, comp):
        fill_inner_area(data, output_grid, comp)
        fill_outer_area(data, output_grid, comp)
      else:
        print(f"Component {idx} is not a closed shape")

    save_grid(output_grid, output_path + "output_grid.json")
    check_and_plot(output_grid, true_output)
   
solve()
