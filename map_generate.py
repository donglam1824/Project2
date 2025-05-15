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
    # Tạo bản đồ trống
    map_grid = np.zeros((size, size), dtype=int)
    
    # Thêm chướng ngại vật
    rows, cols = map_grid.shape
    num_obstacles = int(rows * cols * obstacle_ratio)
    
    # Chọn ngẫu nhiên các vị trí để đặt chướng ngại vật
    obstacle_indices = np.random.choice(rows * cols, num_obstacles, replace=False)
    
    for idx in obstacle_indices:
        r = idx // cols
        c = idx % cols
        map_grid[r, c] = 1

    return map_grid

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

def map_to_string(map_grid, start_pos):
    """
    Chuyển đổi bản đồ thành chuỗi để hiển thị hoặc lưu vào file
    """
    map_str = ""
    for i, row in enumerate(map_grid):
        row_str = []
        for j, cell in enumerate(row):
            if (i, j) == start_pos:
                row_str.append("*")
            else:
                row_str.append(str(cell))
        map_str += " ".join(row_str) + "\n"
    return map_str

def save_map_to_file(map_grid, size, start_pos):
    """
    Lưu bản đồ vào file txt
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"input_map.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(map_to_string(map_grid, start_pos))
    
    return filename, timestamp

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
    
    # Tạo bản đồ
    map_grid = create_square_map(size, obstacle_ratio)
    
    # In bản đồ ra console
    print(f"\n{size}x{size} (ostacel ratio {obstacle_ratio:.1%}):")
    print(map_to_string(map_grid, None))
    
    # Lưu bản đồ vào file
    filename, timestamp = save_map_to_file(map_grid, size, None)
    print(f"\nMap written: {filename}")
            

if __name__ == "__main__":
    main()