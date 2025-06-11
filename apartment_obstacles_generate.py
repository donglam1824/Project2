import numpy as np
import matplotlib.pyplot as plt
import random

def add_obstacles_to_room(grid, room_x, room_y, room_w, room_h, obstacle_ratio=0.1):
    """Thêm chướng ngại vật vào trong phòng"""
    room_area = (room_w - 2) * (room_h - 2)  # Trừ tường
    num_obstacles = int(room_area * obstacle_ratio)
    
    # Chỉ đặt chướng ngại vật ở phần trong của phòng (tránh tường và cửa)
    for _ in range(num_obstacles):
        for attempt in range(10):  # Số lần thử đặt chướng ngại vật
            x = random.randint(room_x + 2, room_x + room_w - 3)
            y = random.randint(room_y + 2, room_y + room_h - 3)
            
            # Kiểm tra xem vị trí này và các ô xung quanh có phù hợp không
            can_place = True
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if grid[y + dy, x + dx] == 1:
                        can_place = False
                        break
                if not can_place:
                    break
            
            if can_place:
                # Đặt chướng ngại vật
                grid[y, x] = 1
                break

def create_apartment_floorplan_with_obstacles(width=40, height=30):
    """Tạo bản đồ căn hộ với chướng ngại vật trong phòng"""
    # Tạo bản đồ cơ bản trước
    grid = np.zeros((height, width), dtype=int)
    
    # Chia bản đồ thành lưới 3x3 phòng
    room_width = width // 3
    room_height = height // 3
    
    # Tạo tường ngăn giữa các phòng
    for j in range(1, 3):
        wall_x = j * room_width - 1
        if wall_x < width:
            grid[:, wall_x] = 1
    
    for i in range(1, 3):
        wall_y = i * room_height - 1
        if wall_y < height:
            grid[wall_y, :] = 1
    
    # Đặt tường biên
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1
    
    # Tạo cửa giữa các phòng
    for i in range(3):
        for j in range(2):  # Cửa ngang
            wall_y = (i + 1) * room_height - 1
            door_start = j * room_width + random.randint(3, room_width - 6)
            door_width = random.randint(3, 4)
            if wall_y < height:
                grid[wall_y, door_start:door_start + door_width] = 0

    for i in range(2):  # Cửa dọc
        for j in range(3):
            wall_x = (i + 1) * room_width - 1
            door_start = j * room_height + random.randint(3, room_height - 6)
            door_height = random.randint(3, 4)
            if wall_x < width:
                grid[door_start:door_start + door_height, wall_x] = 0
    
    # Thêm chướng ngại vật vào mỗi phòng
    for i in range(3):
        for j in range(3):
            room_x = j * room_width
            room_y = i * room_height
            room_w = room_width - (1 if j < 2 else 0)
            room_h = room_height - (1 if i < 2 else 0)
            add_obstacles_to_room(grid, room_x, room_y, room_w, room_h, 
                                obstacle_ratio=random.uniform(0.05, 0.1))
    
    return grid

def save_map_to_file(grid, filename="apartment_map.txt"):
    with open(filename, "w") as f:
        f.write('\n'.join(' '.join(str(cell) for cell in row) for row in grid))
    print(f"Map saved to {filename}")

def visualize_map(grid):
    plt.figure(figsize=(10, 7))
    plt.imshow(grid, cmap='binary')
    plt.title("Apartment Floor Plan with Obstacles")
    plt.grid(True, color='gray', linestyle='-', linewidth=0.5)
    plt.xticks(np.arange(grid.shape[1]))
    plt.yticks(np.arange(grid.shape[0]))
    plt.tight_layout()
    plt.show()

def main():
    grid = create_apartment_floorplan_with_obstacles()
    save_map_to_file(grid)
    visualize_map(grid)

if __name__ == "__main__":
    main()