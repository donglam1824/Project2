import numpy as np
import matplotlib.pyplot as plt
import time

def create_apartment_map(width=20, height=15, room_min_size=3, room_max_size=6, num_rooms=5):
    """
    Tạo bản đồ dạng căn hộ chung cư với các phòng, tường là số 1, sàn là số 0, mỗi phòng có cửa.
    """
    map_grid = np.ones((height, width), dtype=int)
    rooms = []
    np.random.seed(int(time.time()))

    for _ in range(num_rooms):
        for _ in range(100):
            w = np.random.randint(room_min_size, room_max_size+1)
            h = np.random.randint(room_min_size, room_max_size+1)
            x = np.random.randint(1, width - w - 2)  # chừa tường ngoài
            y = np.random.randint(1, height - h - 2)
            new_room = (x, y, w, h)
            # Kiểm tra trùng phòng (cách nhau ít nhất 1 tường)
            overlap = False
            for rx, ry, rw, rh in rooms:
                if (x < rx + rw + 2 and x + w + 2 > rx and
                    y < ry + rh + 2 and y + h + 2 > ry):
                    overlap = True
                    break
            if not overlap:
                rooms.append(new_room)
                # Đặt sàn phòng
                map_grid[y+1:y+1+h, x+1:x+1+w] = 0
                # Tường phòng (giữ nguyên số 1)
                break
    # Tạo cửa cho mỗi phòng (1 cửa trên tường phòng)
    for idx, (x, y, w, h) in enumerate(rooms):
        # Chọn ngẫu nhiên cạnh để đặt cửa
        wall = np.random.choice(['top', 'bottom', 'left', 'right'])
        if wall == 'top':
            cx = np.random.randint(x+1, x+1+w)
            cy = y
        elif wall == 'bottom':
            cx = np.random.randint(x+1, x+1+w)
            cy = y+1+h
        elif wall == 'left':
            cx = x
            cy = np.random.randint(y+1, y+1+h)
        else:  # right
            cx = x+1+w
            cy = np.random.randint(y+1, y+1+h)
        map_grid[cy, cx] = 0
        # Nếu không phải phòng đầu tiên, nối cửa này với cửa phòng trước bằng đường đi nhỏ
        if idx > 0:
            px, py, _, _ = rooms[idx-1]
            # Tìm cửa phòng trước
            prev_doors = np.argwhere(map_grid[py:py+h+2, px:px+w+2] == 0)
            if len(prev_doors) > 0:
                pdy, pdx = prev_doors[0]
                pdy += py
                pdx += px
                # Nối hai cửa bằng đường đi nhỏ (dùng BFS hoặc đường thẳng đơn giản)
                if abs(cx - pdx) > abs(cy - pdy):
                    for ix in range(min(cx, pdx), max(cx, pdx)+1):
                        map_grid[cy, ix] = 0
                    for iy in range(min(cy, pdy), max(cy, pdy)+1):
                        map_grid[iy, pdx] = 0
                else:
                    for iy in range(min(cy, pdy), max(cy, pdy)+1):
                        map_grid[iy, cx] = 0
                    for ix in range(min(cx, pdx), max(cx, pdx)+1):
                        map_grid[pdy, ix] = 0
    # Đảm bảo tường ngoài dày 1
    map_grid[0, :] = 1
    map_grid[-1, :] = 1
    map_grid[:, 0] = 1
    map_grid[:, -1] = 1
    return map_grid

def map_to_string(map_grid):
    return '\n'.join(' '.join(str(cell) for cell in row) for row in map_grid)

def save_map_to_file(map_grid, filename="apartment_map.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(map_to_string(map_grid))
    print(f"Map saved to {filename}")

def visualize_map(map_grid):
    plt.figure(figsize=(8, 6))
    plt.imshow(map_grid, cmap='binary')
    plt.title("Apartment Map")
    plt.grid(True, color='gray', linestyle='-', linewidth=0.5)
    plt.xticks(np.arange(map_grid.shape[1]))
    plt.yticks(np.arange(map_grid.shape[0]))
    plt.tight_layout()
    plt.show()

def main():
    width, height = 20, 15
    # Tăng diện tích phòng: min 5, max 9
    map_grid = create_apartment_map(width, height, room_min_size=5, room_max_size=9, num_rooms=6)
    print(map_to_string(map_grid))
    save_map_to_file(map_grid)
    visualize_map(map_grid)

if __name__ == "__main__":
    main()
