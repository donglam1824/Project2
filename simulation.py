import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

# Read the map from the file we just created
def read_map_file(file_path):
    with open(file_path, 'r') as file:
        map_data = file.read().strip()
    
    # Split data by lines
    map_lines = map_data.splitlines()
    
    # Determine rows and columns
    n_rows = len(map_lines)
    n_cols = len(map_lines[0].split())
    
    grid_map = []
    for line in map_lines:
        grid_map.append(line.split())
    
    return np.array(grid_map), n_rows, n_cols

# Read waypoints from file
def read_waypoints_file(file_path):
    with open(file_path, 'r') as file:
        path_data = file.read().strip()
    
    path_coords = []
    for line in path_data.splitlines():
        # Split x,y coordinates
        line = line.strip('()')
        x, y = map(int, line.split(','))
        path_coords.append((x, y))
    return path_coords

# Read map from file
grid_map, n_rows, n_cols = read_map_file('input_map.txt')

# Convert characters to numbers for visualization
numeric_map = np.zeros((n_rows, n_cols), dtype=int)
start_pos = None

for i in range(n_rows):
    for j in range(n_cols):
        if grid_map[i, j] == '1':
            numeric_map[i, j] = 1  # Obstacle
        elif grid_map[i, j] == '*':
            numeric_map[i, j] = 2  # Starting point
            start_pos = (i, j)
        else:
            numeric_map[i, j] = 0  # Empty path

# Read waypoints
path_coords = read_waypoints_file('waypoint_gpt.txt')

# Create visualization
plt.figure(figsize=(12, 10))
ax = plt.gca()

# Define colors for map elements
colors = ['#FFFFFF', '#F44336', '#4CAF50']  # White for paths, green for start, red for obstacles
cmap = ListedColormap(colors)


plt.pcolormesh(numeric_map, cmap=cmap, edgecolors='k', linewidth=1.5)

# Draw robot path
x_coords = [coord[1] for coord in path_coords]
y_coords = [coord[0] for coord in path_coords]

# Add 0.5 to place path in center of cells and flip y-coordinates
x_plot = [x + 0.5 for x in x_coords]
# Flip the y-coordinates to match the flipped map
y_plot = [y + 0.5 for y in y_coords]

# Draw path with highlighting
plt.plot(x_plot, y_plot, '-', linewidth=3, color='#2196F3', alpha=0.8)  # Blue path

# Mark points along the path
plt.scatter(x_plot, y_plot, c=range(len(x_plot)), cmap='Blues', s=40, 
           zorder=3, edgecolors='navy', linewidth=1)

# Highlight start and end points
plt.plot(x_plot[0], y_plot[0], 'o', markersize=12, markerfacecolor='#4CAF50', 
         markeredgecolor='black', markeredgewidth=1.5)

# Show symbol for starting point
if start_pos:
    plt.text(start_pos[1] + 0.5, start_pos[0] + 0.5, '*', ha='center', va='center', 
             fontsize=24, color='white', fontweight='bold')

# Add coordinate labels
plt.xticks(np.arange(0.5, n_cols + 0.5, 1), [str(i) for i in range(n_cols)])
plt.yticks(np.arange(0.5, n_rows + 0.5, 1), [str(i) for i in range(n_rows)])

# Add grid lines
plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.4, color='gray')

# Add label for start point
plt.text(x_plot[0] + 0.3, y_plot[0] + 0.3, 'Start', fontsize=10, fontweight='bold')

# Adjust axis limits - FIXED: Now using correct orientation
plt.xlim(0, n_cols)
plt.ylim(n_rows, 0)

# Move X-axis to the top
plt.gca().xaxis.set_ticks_position('top')

# Add title and labels
plt.title('Mô phỏng đường đi robot trên bản đồ', fontsize=16, pad=15)
plt.xlabel('X', fontsize=12)
plt.ylabel('Y', fontsize=12)

# Add information about path length
path_length = len(path_coords) - 1
plt.figtext(0.5, 0.01, f'Tổng chiều dài đường đi: {path_length} đơn vị', 
            ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))

# Create legend
obstacle_patch = mpatches.Patch(color='#707070', label='Vật cản (1)')
start_patch = mpatches.Patch(color='#4CAF50', label='Điểm khởi đầu (*)')
path_patch = mpatches.Patch(color='#F0F0F0', label='Đường đi trống (0)')
plt.legend(handles=[obstacle_patch, start_patch, path_patch], 
           loc='upper right', bbox_to_anchor=(1.1, 1.02))

plt.tight_layout()
plt.show()
