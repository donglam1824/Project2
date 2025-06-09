import numpy as np
import matplotlib.pyplot as plt
import random

def check_room_has_door(grid, room_x, room_y, room_width, room_height):
    """Kiểm tra xem phòng có cửa hay không"""
    
    # Kiểm tra tường trên (nếu không phải phòng ở hàng đầu tiên)
    if room_y > 0:
        wall_y = room_y
        for x in range(room_x + 1, room_x + room_width - 1):
            if x < grid.shape[1] and grid[wall_y, x] == 0:
                return True
    
    # Kiểm tra tường dưới (nếu không phải phòng ở hàng cuối cùng)
    if room_y + room_height < grid.shape[0] - 1:
        wall_y = room_y + room_height - 1
        for x in range(room_x + 1, room_x + room_width - 1):
            if x < grid.shape[1] and grid[wall_y, x] == 0:
                return True
    
    # Kiểm tra tường trái (nếu không phải phòng ở cột đầu tiên)
    if room_x > 0:
        wall_x = room_x
        for y in range(room_y + 1, room_y + room_height - 1):
            if y < grid.shape[0] and grid[y, wall_x] == 0:
                return True
    
    # Kiểm tra tường phải (nếu không phải phòng ở cột cuối cùng)
    if room_x + room_width < grid.shape[1] - 1:
        wall_x = room_x + room_width - 1
        for y in range(room_y + 1, room_y + room_height - 1):
            if y < grid.shape[0] and grid[y, wall_x] == 0:
                return True
    
    return False

def get_room_walls_without_doors(grid, room_x, room_y, room_width, room_height):
    """Trả về danh sách các tường của phòng chưa có cửa"""
    walls_without_doors = []
    
    # Kiểm tra tường trên
    if room_y > 0:
        wall_y = room_y
        has_door = False
        for x in range(room_x + 1, room_x + room_width - 1):
            if x < grid.shape[1] and grid[wall_y, x] == 0:
                has_door = True
                break
        if not has_door:
            walls_without_doors.append(('top', wall_y, room_x + 1, room_x + room_width - 1))
    
    # Kiểm tra tường dưới
    if room_y + room_height < grid.shape[0] - 1:
        wall_y = room_y + room_height - 1
        has_door = False
        for x in range(room_x + 1, room_x + room_width - 1):
            if x < grid.shape[1] and grid[wall_y, x] == 0:
                has_door = True
                break
        if not has_door:
            walls_without_doors.append(('bottom', wall_y, room_x + 1, room_x + room_width - 1))
    
    # Kiểm tra tường trái
    if room_x > 0:
        wall_x = room_x
        has_door = False
        for y in range(room_y + 1, room_y + room_height - 1):
            if y < grid.shape[0] and grid[y, wall_x] == 0:
                has_door = True
                break
        if not has_door:
            walls_without_doors.append(('left', wall_x, room_y + 1, room_y + room_height - 1))
    
    # Kiểm tra tường phải
    if room_x + room_width < grid.shape[1] - 1:
        wall_x = room_x + room_width - 1
        has_door = False
        for y in range(room_y + 1, room_y + room_height - 1):
            if y < grid.shape[0] and grid[y, wall_x] == 0:
                has_door = True
                break
        if not has_door:
            walls_without_doors.append(('right', wall_x, room_y + 1, room_y + room_height - 1))
    
    return walls_without_doors

def create_door_in_wall(grid, wall_info):
    """Tạo cửa trong tường được chỉ định"""
    direction, wall_pos, start_pos, end_pos = wall_info
    
    if start_pos >= end_pos:
        return False
    
    # Tạo cửa rộng 2-3 ô
    door_width = min(3, end_pos - start_pos)
    if door_width < 2:
        door_width = 2
    
    # Chọn vị trí ngẫu nhiên cho cửa
    max_start = end_pos - door_width
    if max_start <= start_pos:
        door_start = start_pos
    else:
        door_start = random.randint(start_pos, max_start)
    
    # Tạo cửa
    if direction in ['top', 'bottom']:
        for x in range(door_start, min(door_start + door_width, grid.shape[1])):
            if x < grid.shape[1]:
                grid[wall_pos, x] = 0
    else:  # left, right
        for y in range(door_start, min(door_start + door_width, grid.shape[0])):
            if y < grid.shape[0]:
                grid[y, wall_pos] = 0
    
    return True

def create_apartment_floorplan(width=40, height=30, num_rooms=8):
    """
    Tạo bản đồ mặt sàn chung cư với đảm bảo mỗi phòng có ít nhất 1 cửa
    """
    # Khởi tạo bản đồ trống (tất cả là 0)
    grid = np.zeros((height, width), dtype=int)
    
    # Chia bản đồ thành lưới 3x3 phòng
    room_width = width // 3
    room_height = height // 3
    
    # Tạo các tường ngăn giữa các phòng
    # Tường dọc
    for j in range(1, 3):
        wall_x = j * room_width - 1
        if wall_x < width:
            grid[:, wall_x] = 1
    
    # Tường ngang
    for i in range(1, 3):
        wall_y = i * room_height - 1
        if wall_y < height:
            grid[wall_y, :] = 1
    
    # Đặt tường biên
    grid[0, :] = 1  # Tường trên
    grid[-1, :] = 1  # Tường dưới
    grid[:, 0] = 1  # Tường trái
    grid[:, -1] = 1  # Tường phải
    
    # Danh sách các phòng
    rooms = []
    for i in range(3):
        for j in range(3):
            x = j * room_width
            y = i * room_height
            w = room_width - (1 if j < 2 else 0)
            h = room_height - (1 if i < 2 else 0)
            rooms.append((x, y, w, h))
    
    # Tạo cửa ngẫu nhiên giữa các phòng
    max_attempts = 50
    for attempt in range(max_attempts):
        # Reset grid về trạng thái chỉ có tường
        temp_grid = grid.copy()
        
        # Tạo cửa ngẫu nhiên
        # Cửa ngang (giữa các hàng phòng)
        for i in range(1, 3):
            wall_y = i * room_height - 1
            for j in range(3):
                room_start_x = j * room_width
                room_end_x = room_start_x + room_width - (1 if j < 2 else 0)
                
                # Tạo cửa với xác suất 70%
                if random.random() < 0.7:
                    door_width = random.randint(2, 4)
                    door_start = random.randint(room_start_x + 2, 
                                              max(room_start_x + 2, room_end_x - door_width - 2))
                    for x in range(door_start, min(door_start + door_width, room_end_x)):
                        if x < width:
                            temp_grid[wall_y, x] = 0
        
        # Cửa dọc (giữa các cột phòng)
        for j in range(1, 3):
            wall_x = j * room_width - 1
            for i in range(3):
                room_start_y = i * room_height
                room_end_y = room_start_y + room_height - (1 if i < 2 else 0)
                
                # Tạo cửa với xác suất 70%
                if random.random() < 0.7:
                    door_height = random.randint(2, 4)
                    door_start = random.randint(room_start_y + 2,
                                              max(room_start_y + 2, room_end_y - door_height - 2))
                    for y in range(door_start, min(door_start + door_height, room_end_y)):
                        if y < height:
                            temp_grid[y, wall_x] = 0
        
        # Kiểm tra và bổ sung cửa cho các phòng chưa có cửa
        all_rooms_connected = True
        for idx, (room_x, room_y, room_w, room_h) in enumerate(rooms):
            if not check_room_has_door(temp_grid, room_x, room_y, room_w, room_h):
                # Phòng chưa có cửa, tạo cửa cho phòng này
                walls_without_doors = get_room_walls_without_doors(temp_grid, room_x, room_y, room_w, room_h)
                if walls_without_doors:
                    # Chọn một tường ngẫu nhiên để tạo cửa
                    wall_to_create_door = random.choice(walls_without_doors)
                    create_door_in_wall(temp_grid, wall_to_create_door)
        
        # Kiểm tra lại tất cả các phòng
        all_rooms_connected = True
        for room_x, room_y, room_w, room_h in rooms:
            if not check_room_has_door(temp_grid, room_x, room_y, room_w, room_h):
                all_rooms_connected = False
                break
        
        if all_rooms_connected:
            grid = temp_grid
            break
    
    # Nếu vẫn có phòng chưa có cửa sau tất cả attempts, force tạo cửa
    for room_x, room_y, room_w, room_h in rooms:
        if not check_room_has_door(grid, room_x, room_y, room_w, room_h):
            walls_without_doors = get_room_walls_without_doors(grid, room_x, room_y, room_w, room_h)
            if walls_without_doors:
                wall_to_create_door = walls_without_doors[0]  # Chọn tường đầu tiên
                create_door_in_wall(grid, wall_to_create_door)
    
    return grid

def map_to_string(grid):
    return '\n'.join(' '.join(str(cell) for cell in row) for row in grid)

def save_map_to_file(grid, filename="apartment_map.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(map_to_string(grid))
    print(f"Map saved to {filename}")

def visualize_map(grid):
    plt.figure(figsize=(10, 7))
    plt.imshow(grid, cmap='binary')
    plt.title("Apartment Floor Plan")
    plt.grid(True, color='gray', linestyle='-', linewidth=0.5)
    plt.xticks(np.arange(grid.shape[1]))
    plt.yticks(np.arange(grid.shape[0]))
    plt.tight_layout()
    plt.show()

def verify_all_rooms_connected(grid):
    """Kiểm tra và in thông tin về việc kết nối của các phòng"""
    room_width = grid.shape[1] // 3
    room_height = grid.shape[0] // 3
    
    print("=== ROOM CONNECTION VERIFICATION ===")
    all_connected = True
    
    for i in range(3):
        for j in range(3):
            room_x = j * room_width
            room_y = i * room_height
            room_w = room_width - (1 if j < 2 else 0)
            room_h = room_height - (1 if i < 2 else 0)
            room_number = i * 3 + j + 1
            
            has_door = check_room_has_door(grid, room_x, room_y, room_w, room_h)
            status = "✓ CONNECTED" if has_door else "✗ ISOLATED"
            print(f"Room {room_number} (Row {i+1}, Col {j+1}): {status}")
            
            if not has_door:
                all_connected = False
    
    print(f"\nOverall Status: {'✓ ALL ROOMS CONNECTED' if all_connected else '✗ SOME ROOMS ISOLATED'}")
    return all_connected

def main():
    grid = create_apartment_floorplan()
    print(map_to_string(grid))
    save_map_to_file(grid)
    # visualize_map(grid)

if __name__ == "__main__":
    main()