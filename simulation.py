import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
from waypoint_evaluation import WaypointEvaluator

# Initialize the WaypointEvaluator class
evaluator = WaypointEvaluator('input_map.txt', 'waypoint_gpt.txt', 'lawnmower.xlsx')

# Validate the path
# if not evaluator.is_valid_path():
#     print("Invalid path. Exiting simulation.")
#     exit()

# Evaluate the waypoints
total_distance, coverage_ratio = evaluator.evaluate_waypoints()

# Save evaluation results to Excel
# evaluator.save_to_excel()

# Create visualization
plt.figure(figsize=(12, 10))
ax = plt.gca()

# Define colors for map elements
colors = ['#FFFFFF', '#F44336', '#4CAF50']  # White for paths, green for start, red for obstacles
cmap = ListedColormap(colors)

plt.pcolormesh(evaluator.map_grid, cmap=cmap, edgecolors='k', linewidth=1.5)

# Draw robot path
x_coords = [coord[1] for coord in evaluator.waypoints]
y_coords = [coord[0] for coord in evaluator.waypoints]

# Add 0.5 to place path in center of cells and flip y-coordinates
x_plot = [x + 0.5 for x in x_coords]
y_plot = [y + 0.5 for y in y_coords]

# Draw path with highlighting
plt.plot(x_plot, y_plot, '-', linewidth=3, color='#2196F3', alpha=0.8)  # Blue path

# Mark points along the path
plt.scatter(x_plot, y_plot, c=range(len(x_plot)), cmap='Blues', s=40, 
           zorder=3, edgecolors='navy', linewidth=1)

# Adjust the y-axis to flip the map so (0, 0) is at the top-left corner
plt.gca().invert_yaxis()

# Add text to display coverage ratio and path length on the visualization
coverage_text = f"Coverage: {coverage_ratio:.2%}\nPath Length: {total_distance}"
plt.text(0.02, 0.98, coverage_text, transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))

# Add logic to save the map image with date and time if coverage is not 100%
from datetime import datetime

# Save the map image if coverage is not 100%
if coverage_ratio < 1.0:
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_image_path = f'coverage_map_{current_time}.png'
    plt.savefig(output_image_path)
    print(f"Coverage is not 100%. Map image saved to {output_image_path}")

plt.tight_layout()
plt.show()
