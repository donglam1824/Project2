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

def place_charging_stations(grid):
    """Đặt 5 điểm sạc: 4 ở góc và 1 ở giữa"""
    height, width = grid.shape
    charging_stations = []
    
    # Tìm vị trí phù hợp cho điểm sạc ở 4 góc
    corners = [
        (2, 2),  # Góc trên trái
        (2, width - 3),  # Góc trên phải
        (height - 3, 2),  # Góc dưới trái
        (height - 3, width - 3)  # Góc dưới phải
    ]
    
    # Đặt điểm sạc ở 4 góc
    for y, x in corners:
        # Tìm vị trí trống gần nhất
        found = False
        for radius in range(5):  # Tìm trong bán kính 5 ô
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    ny, nx = y + dy, x + dx
                    if (0 <= ny < height and 0 <= nx < width and 
                        grid[ny, nx] == 0):  # Ô trống
                        grid[ny, nx] = 2  # Đánh dấu là điểm sạc
                        charging_stations.append((ny, nx))
                        found = True
                        break
                if found:
                    break
            if found:
                break
    
    # Đặt điểm sạc ở giữa
    center_y, center_x = height // 2, width // 2
    found = False
    for radius in range(10):  # Tìm trong bán kính 10 ô
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                ny, nx = center_y + dy, center_x + dx
                if (0 <= ny < height and 0 <= nx < width and 
                    grid[ny, nx] == 0):  # Ô trống
                    grid[ny, nx] = 2  # Đánh dấu là điểm sạc
                    charging_stations.append((ny, nx))
                    found = True
                    break
            if found:
                break
        if found:
            break
    
    return charging_stations

def create_apartment_with_charging_stations(width=40, height=30):
    """Tạo bản đồ căn hộ với chướng ngại vật và điểm sạc"""
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
                                obstacle_ratio=random.uniform(0.03, 0.08))
    
    # Đặt 5 điểm sạc
    charging_stations = place_charging_stations(grid)
    
    return grid, charging_stations

def save_map_to_file(grid, filename="apartment_map.txt"):
    """Lưu bản đồ với ký hiệu:
    0 = ô trống
    1 = tường/chướng ngại vật
    2 = điểm sạc
    """
    with open(filename, "w") as f:
        f.write('\n'.join(' '.join(str(cell) for cell in row) for row in grid))
    print(f"Map with charging stations saved to {filename}")

def save_charging_stations_info(charging_stations, filename="charging_stations.txt"):
    """Lưu thông tin vị trí các điểm sạc"""
    with open(filename, "w") as f:
        f.write("Charging Station Positions:\n")
        for i, (y, x) in enumerate(charging_stations, 1):
            f.write(f"Station {i}: ({y}, {x})\n")
    print(f"Charging stations info saved to {filename}")

def visualize_map_with_charging(grid):
    """Hiển thị bản đồ với điểm sạc"""
    plt.figure(figsize=(12, 8))
    
    # Tạo colormap tùy chỉnh
    colors = ['white', 'black', 'red']  # 0=trắng (trống), 1=đen (tường), 2=đỏ (sạc)
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(colors)
    
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=2)
    plt.title("Apartment Floor Plan with Obstacles and Charging Stations")
    plt.grid(True, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
    
    # Thêm legend
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor='white', edgecolor='black', label='Empty'),
        plt.Rectangle((0,0),1,1, facecolor='black', label='Wall/Obstacle'),
        plt.Rectangle((0,0),1,1, facecolor='red', label='Charging Station')
    ]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    plt.xticks(np.arange(grid.shape[1]))
    plt.yticks(np.arange(grid.shape[0]))
    plt.tight_layout()
    plt.show()

def print_charging_stations_info(charging_stations):
    """In thông tin các điểm sạc"""
    print("\n=== CHARGING STATIONS INFO ===")
    station_names = ["Top-Left Corner", "Top-Right Corner", "Bottom-Left Corner", 
                    "Bottom-Right Corner", "Center"]
    
    for i, (y, x) in enumerate(charging_stations):
        name = station_names[i] if i < len(station_names) else f"Station {i+1}"
        print(f"{name}: Position ({y}, {x})")

def main():
    print("Generating apartment map with charging stations...")
    grid, charging_stations = create_apartment_with_charging_stations()
    
    # Lưu bản đồ và thông tin điểm sạc
    save_map_to_file(grid)
    save_charging_stations_info(charging_stations)
    
    # In thông tin điểm sạc
    print_charging_stations_info(charging_stations)
    
    # Hiển thị bản đồ (bỏ comment dòng dưới để xem)
    # visualize_map_with_charging(grid)
    
    print(f"\nMap created with {len(charging_stations)} charging stations")
    print("Map values: 0=Empty, 1=Wall/Obstacle, 2=Charging Station")

if __name__ == "__main__":
    main()