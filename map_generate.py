import numpy as np
import matplotlib.pyplot as plt
import os
import time
import random
from collections import deque
from dotenv import load_dotenv
from google import genai

load_dotenv()

def create_square_map(size, obstacle_ratio=0.2, max_attempts=50):
    """
    Tạo bản đồ hình vuông với kích thước size x size và thêm chướng ngại vật
    size: kích thước bản đồ (n x n)
    obstacle_ratio: tỷ lệ ô bị chặn (từ 0 đến 1)
    max_attempts: số lần thử tối đa để tạo bản đồ hợp lệ
    
    Trả về: Ma trận bản đồ với 0 là ô trống và 1 là chướng ngại vật
    """
    # Đảm bảo obstacle_ratio không quá thấp (để tránh đệ quy vô hạn)
    if obstacle_ratio < 0.05:
        print(f"Obstacle ratio too low ({obstacle_ratio:.2f}), using minimum value (0.05)")
        obstacle_ratio = 0.05
    
    # Điểm bắt đầu và kết thúc cố định
    start_pos = (0, 0)
    end_pos = (size-1, size-1)
    
    for attempt in range(max_attempts):
        # Tạo bản đồ trống
        map_grid = np.zeros((size, size), dtype=int)
        
        # Đảm bảo điểm bắt đầu (0,0) và điểm kết thúc (size-1, size-1) không có chướng ngại vật
        valid_indices = [(r, c) for r in range(size) for c in range(size) 
                         if (r, c) != start_pos and (r, c) != end_pos]
        
        # Tính số chướng ngại vật cần đặt
        num_obstacles = int(size * size * obstacle_ratio)
        
        # Đảm bảo không đặt quá nhiều chướng ngại vật
        num_obstacles = min(num_obstacles, len(valid_indices) - 1)
        
        # Chọn ngẫu nhiên vị trí để đặt chướng ngại vật (không bao gồm start & end)
        obstacle_positions = random.sample(valid_indices, num_obstacles)
        
        # Đặt chướng ngại vật vào bản đồ
        for r, c in obstacle_positions:
            map_grid[r, c] = 1
        
        # Kiểm tra xem có đường đi từ điểm xuất phát đến điểm kết thúc hay không
        if check_path_exists(map_grid, start_pos, end_pos):
            return map_grid, start_pos, end_pos
        
        # Nếu không tìm thấy đường đi, thử lại với bản đồ mới
        print(f"Try {attempt + 1}: Not valid path from start to end.")
    
    # Nếu đã thử nhiều lần mà không thành công, giảm tỷ lệ chướng ngại vật và thông báo
    print(f"Can not generate after {max_attempts} attempts with obstacle ratio {obstacle_ratio:.2f}.")
    print("Creating an almost empty map to ensure a valid path exists.")
    
    # Tạo một bản đồ gần như trống để đảm bảo có đường đi
    map_grid = np.zeros((size, size), dtype=int)
    
    # Thêm một số ít chướng ngại vật (5%) nhưng tránh start và end
    min_obstacle_ratio = 0.05
    valid_indices = [(r, c) for r in range(size) for c in range(size) 
                    if (r, c) != start_pos and (r, c) != end_pos]
    
    min_obstacles = int(min(size * size * min_obstacle_ratio, len(valid_indices) * 0.5))
    obstacle_positions = random.sample(valid_indices, min_obstacles)
    
    for r, c in obstacle_positions:
        map_grid[r, c] = 1
    
    # Đảm bảo có đường đi
    if not check_path_exists(map_grid, start_pos, end_pos):
        # Nếu vẫn không có đường đi, tạo bản đồ hoàn toàn trống
        map_grid = np.zeros((size, size), dtype=int)
    
    return map_grid, start_pos, end_pos

def check_path_exists(map_grid, start_pos, end_pos):
    """
    Kiểm tra xem có đường đi từ điểm xuất phát đến điểm kết thúc hay không
    Sử dụng thuật toán BFS (Breadth-First Search)
    """
    rows, cols = map_grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    
    # Các hướng di chuyển: lên, xuống, trái, phải
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Hàng đợi để BFS
    queue = deque([start_pos])
    visited[start_pos] = True
    
    while queue:
        row, col = queue.popleft()
        
        # Nếu đã đến điểm kết thúc
        if (row, col) == end_pos:
            return True
        
        # Thử các hướng di chuyển
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Kiểm tra xem vị trí mới có hợp lệ không
            if (0 <= new_row < rows and 0 <= new_col < cols and 
                not visited[new_row, new_col] and map_grid[new_row, new_col] == 0):
                queue.append((new_row, new_col))
                visited[new_row, new_col] = True
    
    # Nếu không tìm thấy đường đi
    return False

def visualize_map(map_grid, start_pos, end_pos, path=None):
    """
    Hiển thị bản đồ bằng matplotlib
    0: ô trống (trắng)
    1: chướng ngại vật (đen)
    *: điểm xuất phát (đỏ)
    #: điểm kết thúc (xanh lá)
    """
    plt.figure(figsize=(6, 6))
    plt.imshow(map_grid, cmap='binary')

    # Hiển thị đường đi nếu có
    if path:
        path_y, path_x = zip(*path)
        plt.plot(path_x, path_y, 'b-', linewidth=2)

    # Đánh dấu điểm xuất phát
    plt.plot(start_pos[1], start_pos[0], 'r*', markersize=10)

    # Điểm kết thúc (xanh lá)
    plt.plot(end_pos[1], end_pos[0], 'g#', markersize=15)
    
    # Thêm lưới
    plt.grid(True, color='gray', linestyle='-', linewidth=0.5)
    
    # Hiển thị số hàng và cột
    plt.xticks(np.arange(map_grid.shape[1]))
    plt.yticks(np.arange(map_grid.shape[0]))
    
    plt.tight_layout()
    plt.show()

def map_to_string(map_grid, start_pos, end_pos):
    """
    Chuyển đổi bản đồ thành chuỗi để hiển thị hoặc lưu vào file
    """
    map_str = ""
    for i, row in enumerate(map_grid):
        row_str = []
        for j, cell in enumerate(row):
            if (i, j) == start_pos:
                row_str.append("*")  # Điểm xuất phát
            elif (i, j) == end_pos:
                row_str.append("#")  # Điểm kết thúc
            else:
                row_str.append(str(cell))
        map_str += " ".join(row_str) + "\n"
    return map_str

def save_map_to_file(map_grid, size, start_pos, end_pos):
    """
    Lưu bản đồ vào file txt
    """
    filename = f"input_map.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(map_to_string(map_grid, start_pos, end_pos))
    
    return filename, time.strftime("%Y%m%d_%H%M%S")

def find_shortest_path(map_grid, start_pos, end_pos):
    """
    Tìm đường đi ngắn nhất từ điểm xuất phát đến điểm kết thúc
    Sử dụng thuật toán BFS (Breadth-First Search)
    """
    rows, cols = map_grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    
    # Các hướng di chuyển: lên, xuống, trái, phải
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Hàng đợi để BFS
    queue = deque([start_pos])
    visited[start_pos] = True
    
    # Lưu lại đường đi
    parent = {}
    
    while queue:
        row, col = queue.popleft()
        
        # Nếu đã đến điểm kết thúc
        if (row, col) == end_pos:
            # Khôi phục đường đi
            path = []
            current = end_pos
            while current != start_pos:
                path.append(current)
                current = parent[current]
            path.append(start_pos)
            path.reverse()
            return path
        
        # Thử các hướng di chuyển
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Kiểm tra xem vị trí mới có hợp lệ không
            if (0 <= new_row < rows and 0 <= new_col < cols and 
                not visited[new_row, new_col] and map_grid[new_row, new_col] == 0):
                queue.append((new_row, new_col))
                visited[new_row, new_col] = True
                parent[(new_row, new_col)] = (row, col)
    
    # Nếu không tìm thấy đường đi
    return None

def main():
    """
    Hàm chính của chương trình
    """
    # Nhận đầu vào từ người dùng
    # size = int(input("Nhập kích thước n cho bản đồ n x n: "))
    
    # # Kiểm tra giá trị hợp lệ
    # if size < 2:
    #     print("Kích thước bản đồ phải ít nhất là 2x2")
    #     return
    size = 19
    # Sử dụng tỷ lệ chướng ngại vật cố định
    obstacle_ratio = 0.1
    
    # Tạo bản đồ với điểm bắt đầu (0,0) và kết thúc (size-1, size-1)
    map_grid, start_pos, end_pos = create_square_map(size, obstacle_ratio)
    
    # In bản đồ ra console
    print(f"\n{size}x{size} (obstacle ratio {obstacle_ratio:.1%}):")
    print(map_to_string(map_grid, start_pos, end_pos))
    
    # Lưu bản đồ vào file
    filename, timestamp = save_map_to_file(map_grid, size, start_pos, end_pos)
    print(f"\nMap written: {filename}")

if __name__ == "__main__":
    main()