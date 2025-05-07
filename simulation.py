import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

# Đọc bản đồ từ file input_map.txt
def read_map_file(file_path):
    with open(file_path, 'r') as file:
        map_data = file.read().strip()
    
    # Tách dữ liệu theo dòng
    map_lines = map_data.splitlines()
    
    # Xác định số hàng và cột từ dữ liệu
    n_rows = len(map_lines)
    n_cols = len(map_lines[0].split())
    
    grid_map = []
    for line in map_lines:
        grid_map.append(line.split())
    
    return np.array(grid_map), n_rows, n_cols

# Đọc đường đi từ file waypoints_gpt.txt
def read_waypoints_file(file_path):
    with open(file_path, 'r') as file:
        path_data = file.read().strip()
    
    # Loại bỏ dấu ngoặc đơn và tách (x, y)
    path_coords = []
    for line in path_data.splitlines():
        # Loại bỏ dấu ngoặc và tách (x, y)
        line = line.strip('()')
        x, y = map(int, line.split(','))
        path_coords.append((x, y))
    return path_coords

# Đọc bản đồ từ file
grid_map, n_rows, n_cols = read_map_file('input_map.txt')

# Chuyển đổi các ký tự thành số để dễ vẽ
numeric_map = np.zeros((n_rows, n_cols), dtype=int)
start_pos = None
goal_pos = None

for i in range(n_rows):
    for j in range(n_cols):
        if grid_map[i, j] == '1':
            numeric_map[i, j] = 1  # Vật cản
        elif grid_map[i, j] == '*':
            numeric_map[i, j] = 2  # Điểm khởi đầu
            start_pos = (i, j)
        elif grid_map[i, j] == '#':
            numeric_map[i, j] = 3  # Điểm đích
            goal_pos = (i, j)
        else:
            numeric_map[i, j] = 0  # Đường đi trống

# Đọc đường đi từ file
path_coords = read_waypoints_file('waypoint_gpt.txt')

# Tạo hình vẽ
plt.figure(figsize=(12, 10))
ax = plt.gca()

# Tạo bản đồ màu rõ ràng hơn cho các phần tử
colors = ['#F0F0F0', '#707070', '#4CAF50', '#F44336']  # Trắng xám nhạt, xám đậm, xanh lá, đỏ
cmap = ListedColormap(colors)

# Hiển thị bản đồ với các ô lớn hơn và rõ ràng hơn
plt.pcolormesh(numeric_map.T, cmap=cmap, edgecolors='k', linewidth=1.5)

# Vẽ đường đi của robot
x_coords = [coord[0] for coord in path_coords]
y_coords = [coord[1] for coord in path_coords]

# Thêm 0.5 để đặt đường đi vào giữa ô
x_plot = [x + 0.5 for x in x_coords]
y_plot = [y + 0.5 for y in y_coords]

# Vẽ đường đi với màu sắc nổi bật và thêm hiệu ứng gradient
plt.plot(x_plot, y_plot, '-', linewidth=3, color='#2196F3', alpha=0.8)  # Màu xanh dương đẹp

# Đánh dấu các điểm trên đường đi
plt.scatter(x_plot, y_plot, c=range(len(x_plot)), cmap='Blues', s=40, 
           zorder=3, edgecolors='navy', linewidth=1)

# Đánh dấu điểm bắt đầu và kết thúc của đường đi nổi bật hơn
plt.plot(x_plot[0], y_plot[0], 'o', markersize=12, markerfacecolor='#4CAF50', 
         markeredgecolor='black', markeredgewidth=1.5)
plt.plot(x_plot[-1], y_plot[-1], 'o', markersize=12, markerfacecolor='#F44336', 
         markeredgecolor='black', markeredgewidth=1.5)

# Hiển thị ký hiệu cho điểm đầu và điểm cuối
if start_pos:
    plt.text(start_pos[0] + 0.5, start_pos[1] + 0.5, '*', ha='center', va='center', 
             fontsize=24, color='white', fontweight='bold')
if goal_pos:
    plt.text(goal_pos[0] + 0.5, goal_pos[1] + 0.5, '#', ha='center', va='center', 
             fontsize=24, color='white', fontweight='bold')

# Thêm chỉ số tọa độ ở biên để dễ theo dõi (thay vì trên mỗi ô)
plt.xticks(np.arange(0.5, n_rows + 0.5, 1), [str(i) for i in range(n_rows)])
plt.yticks(np.arange(0.5, n_cols + 0.5, 1), [str(i) for i in range(n_cols)])

# Tạo khung lưới nhẹ nhàng hơn
plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.4, color='gray')

# Tùy chọn: Thêm nhãn cho một số điểm quan trọng trên đường đi (điểm đầu, điểm cuối, các điểm rẽ)
plt.text(x_plot[0] + 0.3, y_plot[0] + 0.3, 'Start', fontsize=10, fontweight='bold')
plt.text(x_plot[-1] + 0.3, y_plot[-1] + 0.3, 'Goal', fontsize=10, fontweight='bold')

# # Thêm chú thích
# obstacle_patch = mpatches.Patch(color=colors[1], label='Vật cản (1)')
# free_patch = mpatches.Patch(color=colors[0], label='Đường đi trống (0)')
# start_patch = mpatches.Patch(color=colors[2], label='Điểm xuất phát (*)')
# goal_patch = mpatches.Patch(color=colors[3], label='Điểm đích (#)')
# path_line = plt.Line2D([0], [0], color='#2196F3', lw=3, label='Đường đi robot')

# plt.legend(handles=[obstacle_patch, free_patch, start_patch, goal_patch, path_line], 
#            loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5, frameon=True,
#            fancybox=True, shadow=True)

# Điều chỉnh giới hạn trục
plt.xlim(0, n_rows)
plt.ylim(0, n_cols)

plt.title('Mô phỏng đường đi robot trên bản đồ', fontsize=16, pad=15)
plt.xlabel('X', fontsize=12)
plt.ylabel('Y', fontsize=12)

# Thêm thông tin về đường đi
path_length = len(path_coords) - 1
plt.figtext(0.5, 0.01, f'Tổng chiều dài đường đi: {path_length} đơn vị', 
            ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))

plt.tight_layout()
plt.show()