import logging
from collections import deque

def read_map_from_file(filename):
    map_data = []
    with open(filename, 'r') as file:
        for line in file:
            row = line.strip().split()
            map_data.append(row)
    return map_data

def write_waypoints_to_file(waypoints, filename):
    with open(filename, 'w') as file:
        for waypoint in waypoints:
            file.write(f"{waypoint}\n")

directions_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def find_rooms(map_data):
    """Tìm tất cả các phòng (vùng liên thông) trong bản đồ"""
    rows, cols = len(map_data), len(map_data[0])
    visited = [[False]*cols for _ in range(rows)]
    rooms = []
    
    def bfs_room(start_i, start_j):
        """BFS để tìm tất cả ô trong một phòng"""
        queue = [(start_i, start_j)]
        visited[start_i][start_j] = True
        room_cells = [(start_i, start_j)]
        
        while queue:
            i, j = queue.pop(0)
            for di, dj in directions_4:
                ni, nj = i + di, j + dj
                if (0 <= ni < rows and 0 <= nj < cols and 
                    not visited[ni][nj] and map_data[ni][nj] == '0'):
                    visited[ni][nj] = True
                    queue.append((ni, nj))
                    room_cells.append((ni, nj))
        
        return sorted(room_cells)
    
    for i in range(rows):
        for j in range(cols):
            if map_data[i][j] == '0' and not visited[i][j]:
                room = bfs_room(i, j)
                if len(room) > 1:  # Chỉ lấy phòng có ít nhất 2 ô
                    rooms.append(room)
    
    return rooms

def lawnmower_sweep_room(room_cells):
    """Quét kiểu lawnmower trong một phòng"""
    if not room_cells:
        return []
    
    # Tìm boundaries của phòng
    min_row = min(cell[0] for cell in room_cells)
    max_row = max(cell[0] for cell in room_cells)
    min_col = min(cell[1] for cell in room_cells)
    max_col = max(cell[1] for cell in room_cells)
    
    # Tạo set cho tra cứu nhanh
    room_set = set(room_cells)
    waypoints = []
    
    # Lawnmower theo hàng
    direction = 1  # 1: trái sang phải, -1: phải sang trái
    
    for row in range(min_row, max_row + 1):
        row_cells = []
        
        # Thu thập tất cả ô trong hàng này thuộc phòng
        for col in range(min_col, max_col + 1):
            if (row, col) in room_set:
                row_cells.append((row, col))
        
        if row_cells:
            # Sắp xếp theo hướng quét
            if direction == 1:
                row_cells.sort(key=lambda x: x[1])  # Trái sang phải
            else:
                row_cells.sort(key=lambda x: x[1], reverse=True)  # Phải sang trái
            
            # Thêm các ô vào waypoints với đường đi liên tục
            if waypoints:
                # Tìm đường đi tới ô đầu tiên của hàng mới
                path_to_row = find_path_in_room(room_set, waypoints[-1], row_cells[0])
                if path_to_row and len(path_to_row) > 1:
                    waypoints.extend(path_to_row[1:])  # Bỏ điểm bắt đầu
                elif waypoints[-1] != row_cells[0]:
                    waypoints.append(row_cells[0])
            else:
                waypoints.append(row_cells[0])
            
            # Thêm các ô còn lại trong hàng
            for i in range(1, len(row_cells)):
                current = row_cells[i-1]
                next_cell = row_cells[i]
                
                # Kiểm tra xem có liên tục không
                if abs(current[1] - next_cell[1]) == 1:
                    waypoints.append(next_cell)
                else:
                    # Tìm đường đi liên tục
                    path = find_path_in_room(room_set, current, next_cell)
                    if path and len(path) > 1:
                        waypoints.extend(path[1:])
                    else:
                        waypoints.append(next_cell)
            
            direction *= -1  # Đổi hướng cho hàng tiếp theo
    
    return waypoints

def find_path_in_room(room_set, start, goal):
    """Tìm đường đi ngắn nhất trong phòng bằng BFS"""
    if start == goal:
        return [start]
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        for di, dj in directions_4:
            next_pos = (current[0] + di, current[1] + dj)
            
            if next_pos in room_set and next_pos not in visited:
                new_path = path + [next_pos]
                if next_pos == goal:
                    return new_path
                
                visited.add(next_pos)
                queue.append((next_pos, new_path))
    
    return []  # Không tìm thấy đường đi

def find_path_between_rooms(map_data, start, goal):
    """Tìm đường đi giữa các phòng bằng BFS"""
    rows, cols = len(map_data), len(map_data[0])
    
    if start == goal:
        return [start]
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        for di, dj in directions_4:
            next_pos = (current[0] + di, current[1] + dj)
            ni, nj = next_pos
            
            if (0 <= ni < rows and 0 <= nj < cols and 
                map_data[ni][nj] == '0' and next_pos not in visited):
                
                new_path = path + [next_pos]
                if next_pos == goal:
                    return new_path
                
                visited.add(next_pos)
                queue.append((next_pos, new_path))
    
    return []

def lawnmower_room_priority_planning(map_data):
    """
    Thuật toán lawnmower ưu tiên quét từng phòng:
    1. Tìm tất cả các phòng
    2. Quét kiểu lawnmower trong từng phòng
    3. Di chuyển giữa các phòng
    """
    rows, cols = len(map_data), len(map_data[0])
    
    # Tìm tất cả các phòng
    rooms = find_rooms(map_data)
    
    if not rooms:
        logging.warning("Không tìm thấy phòng nào!")
        return []
    
    logging.info(f"Tìm thấy {len(rooms)} phòng")
    for i, room in enumerate(rooms):
        logging.info(f"Phòng {i+1}: {len(room)} ô")
    
    all_waypoints = []
    
    # Bắt đầu từ phòng đầu tiên
    for room_idx, room in enumerate(rooms):
        logging.info(f"Đang quét phòng {room_idx + 1}...")
        
        # Quét kiểu lawnmower trong phòng
        room_waypoints = lawnmower_sweep_room(room)
        
        if room_idx == 0:
            # Phòng đầu tiên: thêm tất cả waypoints
            all_waypoints.extend(room_waypoints)
        else:
            # Phòng tiếp theo: tìm đường đi từ vị trí hiện tại
            if all_waypoints and room_waypoints:
                current_pos = all_waypoints[-1]
                room_start = room_waypoints[0]
                
                # Tìm đường đi giữa các phòng
                inter_room_path = find_path_between_rooms(map_data, current_pos, room_start)
                
                if inter_room_path and len(inter_room_path) > 1:
                    all_waypoints.extend(inter_room_path[1:])  # Bỏ điểm bắt đầu
                elif current_pos != room_start:
                    all_waypoints.append(room_start)
                
                # Thêm waypoints trong phòng (bỏ điểm đầu nếu đã có)
                if room_waypoints[0] == all_waypoints[-1]:
                    all_waypoints.extend(room_waypoints[1:])
                else:
                    all_waypoints.extend(room_waypoints)
    
    logging.info(f"Tổng cộng tạo ra {len(all_waypoints)} waypoints")
    return all_waypoints

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Đọc bản đồ từ file
    map_data = read_map_from_file('apartment_map.txt')
    logging.info(f"Đã đọc bản đồ kích thước: {len(map_data)}x{len(map_data[0])}")
    
    # Chạy thuật toán lawnmower ưu tiên phòng
    waypoints = lawnmower_room_priority_planning(map_data)
    logging.info(f"Đã tạo {len(waypoints)} waypoints")
    
    # Ghi waypoints ra file
    write_waypoints_to_file(waypoints, 'waypoint_gpt.txt')
    logging.info("Đã ghi waypoints vào file waypoint_gpt.txt")
    
    # In một vài waypoints đầu và cuối để kiểm tra
    if waypoints:
        logging.info("Waypoints đầu tiên:")
        for i in range(min(10, len(waypoints))):
            logging.info(f"  {i+1}: {waypoints[i]}")
        
        if len(waypoints) > 10:
            logging.info("Waypoints cuối cùng:")
            for i in range(max(0, len(waypoints)-5), len(waypoints)):
                logging.info(f"  {i+1}: {waypoints[i]}")

if __name__ == "__main__":
    main()
