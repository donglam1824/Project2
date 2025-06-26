import logging

def read_map_from_file(filename):
    map_data = []
    with open(filename, 'r') as file:
        for line in file:
            row = line.strip().split()
            map_data.append(row)
    return map_data

directions_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_adjacent(pos1, pos2):
    """Kiểm tra hai điểm có liền kề nhau không (chỉ cách nhau 1 ô theo 4 hướng)"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

def find_rooms(map_data):
    """Tìm các phòng riêng biệt trong bản đồ với thông tin chi tiết"""
    rows, cols = len(map_data), len(map_data[0])
    visited = [[False]*cols for _ in range(rows)]
    rooms = []
    
    for i in range(rows):
        for j in range(cols):
            if map_data[i][j] == '0' and not visited[i][j]:
                # BFS để tìm 1 phòng
                queue = [(i, j)]
                room = []
                visited[i][j] = True
                
                while queue:
                    x, y = queue.pop(0)
                    room.append((x, y))
                    for dx, dy in directions_4:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and map_data[nx][ny] == '0' and not visited[nx][ny]:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                
                # Chỉ thêm phòng nếu có kích thước đủ lớn (tránh các ô nhỏ lẻ)
                if len(room) >= 4:  # Tối thiểu 4 ô để được coi là phòng
                    rooms.append(room)
    
    return rooms

def analyze_room_structure(map_data, rooms):
    """Phân tích cấu trúc phòng và tìm cửa ra vào"""
    room_info = []
    
    for idx, room in enumerate(rooms):
        room_set = set(room)
        
        # Tính boundaries của phòng
        min_row = min(pos[0] for pos in room)
        max_row = max(pos[0] for pos in room)
        min_col = min(pos[1] for pos in room)
        max_col = max(pos[1] for pos in room)
        
        # Tìm các cửa ra vào (kết nối với phòng khác)
        doors = find_room_doors(map_data, room, rooms, idx)
        
        # Tính diện tích và tỷ lệ hình dạng
        area = len(room)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        aspect_ratio = max(width, height) / min(width, height) if min(width, height) > 0 else 1
        
        # Xác định loại phòng dựa trên kích thước và hình dạng
        room_type = classify_room_type(area, aspect_ratio, doors)
        
        room_data = {
            'id': idx,
            'cells': room,
            'area': area,
            'bounds': (min_row, max_row, min_col, max_col),
            'width': width,
            'height': height,
            'aspect_ratio': aspect_ratio,
            'doors': doors,
            'room_type': room_type,
            'center': ((min_row + max_row) // 2, (min_col + max_col) // 2)
        }
        
        room_info.append(room_data)
    
    return room_info

def find_room_doors(map_data, current_room, all_rooms, current_room_idx):
    """Tìm các cửa ra vào của phòng (điểm kết nối với phòng khác)"""
    doors = []
    current_room_set = set(current_room)
    
    # Tạo set cho tất cả các phòng khác
    other_rooms_cells = set()
    for idx, room in enumerate(all_rooms):
        if idx != current_room_idx:
            other_rooms_cells.update(room)
    
    # Kiểm tra mỗi ô trong phòng hiện tại
    for x, y in current_room:
        # Kiểm tra 4 hướng xung quanh
        for dx, dy in directions_4:
            nx, ny = x + dx, y + dy
            
            # Nếu ô liền kề thuộc phòng khác, thì (x,y) là cửa
            if (nx, ny) in other_rooms_cells:
                doors.append((x, y))
                break  # Mỗi ô chỉ cần đánh dấu 1 lần
    
    return list(set(doors))  # Loại bỏ trùng lặp

def classify_room_type(area, aspect_ratio, doors):
    """Phân loại loại phòng dựa trên đặc điểm"""
    if area < 10:
        return "small_room"  # Phòng nhỏ
    elif area < 30:
        if aspect_ratio > 3:
            return "corridor"  # Hành lang
        else:
            return "medium_room"  # Phòng vừa
    else:
        if len(doors) > 2:
            return "main_room"  # Phòng chính
        else:
            return "large_room"  # Phòng lớn

def move_step_by_step(room_set, start, goal, visited):
    """Di chuyển từng bước một từ start đến goal, đảm bảo chỉ di chuyển các ô liền kề"""
    if start == goal:
        return [start]
    
    # BFS để tìm đường đi ngắn nhất, chỉ di chuyển các ô liền kề
    queue = [(start, [start])]
    visited_local = set([start])
    
    while queue:
        current, path = queue.pop(0)
        
        if current == goal:
            return path
        
        # Kiểm tra 4 hướng di chuyển (chỉ các ô liền kề)
        for dx, dy in directions_4:
            next_pos = (current[0] + dx, current[1] + dy)
            
            if (next_pos in room_set and 
                next_pos not in visited_local):
                
                visited_local.add(next_pos)
                new_path = path + [next_pos]
                queue.append((next_pos, new_path))
    
    return []

def validate_path_continuity(path):
    """Kiểm tra tính liên tục của đường đi (mỗi bước chỉ cách 1 ô)"""
    if len(path) < 2:
        return True
    
    for i in range(1, len(path)):
        if not is_adjacent(path[i-1], path[i]):
            return False
    return True

def create_smart_lawnmower_path(room, start):
    """Tạo đường đi lawnmower thông minh với khả năng quay đầu khi gặp chướng ngại vật - bắt đầu từ góc trên trái"""
    if not room:
        return []
    
    room_set = set(room)
    path = []
    visited = set()
    
    # Tìm góc trên trái của phòng
    min_row = min(pos[0] for pos in room)
    min_col = min(pos[1] for pos in room)
    
    # Tìm điểm bắt đầu - ưu tiên góc trên trái
    top_left_candidates = [(min_row, col) for col in range(min_col, min_col + 3) 
                          if (min_row, col) in room_set]
    
    if top_left_candidates:
        current = top_left_candidates[0]  # Góc trên trái
    else:
        current = min(room, key=lambda p: p[0] * 1000 + p[1])  # Điểm trên cùng, trái nhất
    
    path.append(current)
    visited.add(current)
    
    # Tìm boundaries của phòng
    max_row = max(pos[0] for pos in room)
    max_col = max(pos[1] for pos in room)
    
    # Pattern lawnmower với quay đầu thông minh - bắt đầu từ trên xuống
    going_right = True
    
    for row in range(min_row, max_row + 1):
        # Tìm các ô hợp lệ trong dòng
        row_cells = [(row, col) for col in range(min_col, max_col + 1) 
                     if (row, col) in room_set]
        
        if not row_cells:
            continue
        
        # Sắp xếp theo hướng di chuyển
        if going_right:
            row_cells.sort(key=lambda x: x[1])  # Sắp xếp theo cột tăng dần (trái -> phải)
        else:
            row_cells.sort(key=lambda x: x[1], reverse=True)  # Giảm dần (phải -> trái)
        
        # Di chuyển đến điểm đầu dòng
        if row_cells and row_cells[0] != current:
            move_path = move_step_by_step(room_set, current, row_cells[0], visited)
            if move_path:
                for pos in move_path[1:]:  # Bỏ qua điểm hiện tại
                    if pos not in visited:
                        path.append(pos)
                        visited.add(pos)
                current = move_path[-1]
        
        # Quét theo dòng với khả năng né chướng ngại vật
        for target_cell in row_cells:
            if target_cell not in visited:
                # Thử di chuyển trực tiếp
                if is_adjacent(current, target_cell):
                    path.append(target_cell)
                    visited.add(target_cell)
                    current = target_cell
                else:
                    # Tìm đường đi gián tiếp
                    move_path = move_step_by_step(room_set, current, target_cell, visited)
                    if move_path:
                        for pos in move_path[1:]:
                            if pos not in visited:
                                path.append(pos)
                                visited.add(pos)
                        current = move_path[-1]
        
        # Chuyển hướng cho dòng tiếp theo
        going_right = not going_right
    
    # Quét các ô còn lại chưa được thăm
    unvisited = room_set - visited
    while unvisited:
        nearest = min(unvisited, key=lambda p: abs(p[0]-current[0]) + abs(p[1]-current[1]))
        move_path = move_step_by_step(room_set, current, nearest, visited)
        
        if move_path:
            for pos in move_path[1:]:
                if pos not in visited:
                    path.append(pos)
                    visited.add(pos)
            current = move_path[-1]
            unvisited.remove(nearest)
        else:
            # Nếu không tìm được đường, loại bỏ ô này
            unvisited.remove(nearest)
    
    return path

def bfs_path_with_obstacle_avoidance(map_data, start, goal):
    """BFS với khả năng né chướng ngại vật cải tiến - chỉ di chuyển từng ô một"""
    rows, cols = len(map_data), len(map_data[0])
    queue = [(start, [start])]
    visited = set([start])
    
    while queue:
        (x, y), path = queue.pop(0)
        if (x, y) == goal:
            # Kiểm tra path có hợp lệ không (di chuyển từng ô một)
            if validate_path_continuity(path):
                return path
            
        # Sử dụng hướng ưu tiên để tránh chướng ngại vật
        preferred_moves = get_preferred_moves((x, y), goal)
        
        for dx, dy in preferred_moves:
            nx, ny = x + dx, y + dy
            if (0 <= nx < rows and 0 <= ny < cols and 
                map_data[nx][ny] == '0' and (nx, ny) not in visited):
                # Đảm bảo chỉ di chuyển từng ô một (kiểm tra adjacent)
                if is_adjacent((x, y), (nx, ny)):
                    visited.add((nx, ny))
                    new_path = path + [(nx, ny)]
                    queue.append(((nx, ny), new_path))
    return []

def get_preferred_moves(current, goal):
    """Trả về các hướng di chuyển theo thứ tự ưu tiên dựa trên vị trí mục tiêu"""
    row_diff = goal[0] - current[0]
    col_diff = goal[1] - current[1]
    
    moves = []
    
    # Ưu tiên di chuyển theo trục có khoảng cách lớn hơn
    if abs(row_diff) > abs(col_diff):
        # Ưu tiên di chuyển theo hàng trước
        if row_diff > 0:
            moves.append((1, 0))   # Xuống
        elif row_diff < 0:
            moves.append((-1, 0))  # Lên
        
        if col_diff > 0:
            moves.append((0, 1))   # Phải
        elif col_diff < 0:
            moves.append((0, -1))  # Trái
    else:
        # Ưu tiên di chuyển theo cột trước
        if col_diff > 0:
            moves.append((0, 1))   # Phải
        elif col_diff < 0:
            moves.append((0, -1))  # Trái
            
        if row_diff > 0:
            moves.append((1, 0))   # Xuống
        elif row_diff < 0:
            moves.append((-1, 0))  # Lên
    
    # Thêm các hướng còn lại
    all_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for direction in all_directions:
        if direction not in moves:
            moves.append(direction)
    
    return moves

def find_best_room_entry_point(room_info, current_pos):
    """Tìm điểm vào tốt nhất cho phòng - ưu tiên góc trên trái"""
    room_cells = room_info['cells']
    doors = room_info['doors']
    
    # Nếu có cửa, ưu tiên cửa gần nhất với góc trên trái
    if doors:
        min_row = min(pos[0] for pos in room_cells)
        min_col = min(pos[1] for pos in room_cells)
        return min(doors, key=lambda d: abs(d[0] - min_row) + abs(d[1] - min_col))
    
    # Nếu không có cửa, chọn góc trên trái của phòng
    min_row = min(pos[0] for pos in room_cells)
    min_col = min(pos[1] for pos in room_cells)
    
    # Tìm điểm gần góc trên trái nhất trong phòng
    top_left_candidate = (min_row, min_col)
    if top_left_candidate in room_cells:
        return top_left_candidate
    
    # Nếu góc trên trái không có, tìm điểm gần nhất với góc trên trái
    return min(room_cells, key=lambda p: abs(p[0] - min_row) + abs(p[1] - min_col))

def remove_duplicate_consecutive_points(waypoints):
    """Loại bỏ các điểm trùng lặp liên tiếp"""
    if not waypoints:
        return []
    
    result = [waypoints[0]]
    for i in range(1, len(waypoints)):
        if waypoints[i] != waypoints[i-1]:
            result.append(waypoints[i])
    
    return result

def write_waypoints_to_file(waypoints, filename):
    """Ghi waypoints vào file với format cải thiện"""
    with open(filename, 'w') as file:
        previous_point = None
        count = 0
        for point in waypoints:
            if previous_point != point:
                file.write(f"({point[0]}, {point[1]})\n")
                previous_point = point
                count += 1
        print(f"Đã ghi {count} waypoints vào file {filename}")

def room_based_lawnmower_path_planning(map_data):
    """Thuật toán di chuyển thông minh với nhận diện phòng từ bản đồ - bắt đầu từ góc trên trái"""
    # Tìm các phòng
    rooms = find_rooms(map_data)
    if not rooms:
        return []
    
    # Phân tích cấu trúc phòng
    room_analysis = analyze_room_structure(map_data, rooms)
    
    waypoints = []
    visited_rooms = set()
    
    # In thông tin phòng để debug
    print("=== ROOM ANALYSIS ===")
    for room_info in room_analysis:
        print(f"Room {room_info['id']}: {room_info['room_type']}")
        print(f"  Area: {room_info['area']} cells")
        print(f"  Bounds: {room_info['bounds']}")
        print(f"  Doors: {len(room_info['doors'])} doors")
        print(f"  Center: {room_info['center']}")
        print()
    
    # Bắt đầu từ góc trên cùng bên trái của bản đồ
    # Tìm ô trống đầu tiên từ góc trên trái
    start_pos = None
    rows, cols = len(map_data), len(map_data[0])
    
    for i in range(rows):
        for j in range(cols):
            if map_data[i][j] == '0':  # Ô trống đầu tiên
                start_pos = (i, j)
                break
        if start_pos:
            break
    
    if not start_pos:
        return []
    
    print(f"Starting from top-left position: {start_pos}")
    
    # Tìm phòng chứa điểm bắt đầu
    start_room = None
    for room_info in room_analysis:
        if start_pos in room_info['cells']:
            start_room = room_info
            break
    
    # Nếu không tìm thấy phòng chứa điểm bắt đầu, chọn phòng gần nhất
    if not start_room:
        start_room = min(room_analysis, 
                        key=lambda r: min(abs(start_pos[0] - cell[0]) + abs(start_pos[1] - cell[1]) 
                                         for cell in r['cells']))
    
    current_pos = start_pos
    
    # Sắp xếp phòng: phòng chứa điểm bắt đầu trước, sau đó sắp xếp theo khoảng cách
    sorted_rooms = []
    
    # Thêm phòng bắt đầu đầu tiên
    sorted_rooms.append(start_room)
    remaining_rooms = [r for r in room_analysis if r['id'] != start_room['id']]
    
    # Sắp xếp các phòng còn lại theo khoảng cách từ điểm hiện tại
    current_room_pos = start_pos
    while remaining_rooms:
        nearest_room = min(remaining_rooms, 
                          key=lambda r: min(abs(current_room_pos[0] - cell[0]) + abs(current_room_pos[1] - cell[1]) 
                                           for cell in r['cells']))
        sorted_rooms.append(nearest_room)
        remaining_rooms.remove(nearest_room)
        # Cập nhật current_pos để sắp xếp phòng tiếp theo
        current_room_pos = nearest_room['center']
    
    for room_info in sorted_rooms:
        if room_info['id'] in visited_rooms:
            continue
            
        print(f"Processing Room {room_info['id']} ({room_info['room_type']})")
        
        # Nếu đây không phải phòng đầu tiên, tìm đường đi đến phòng này
        if waypoints:
            # Tìm điểm vào tốt nhất cho phòng này
            entry_point = find_best_room_entry_point(room_info, current_pos)
            
            # Di chuyển đến điểm vào của phòng
            path_to_room = bfs_path_with_obstacle_avoidance(map_data, current_pos, entry_point)
            
            if path_to_room and validate_path_continuity(path_to_room):
                # Đảm bảo liên tục khi thêm path
                for i, point in enumerate(path_to_room[1:], 1):  
                    if not waypoints or is_adjacent(waypoints[-1], point):
                        waypoints.append(point)
                    else:
                        # Tìm đường kết nối liên tục
                        all_free_cells = set()
                        for row in range(len(map_data)):
                            for col in range(len(map_data[0])):
                                if map_data[row][col] == '0':
                                    all_free_cells.add((row, col))
                        
                        connecting_path = move_step_by_step(all_free_cells, waypoints[-1], point, set())
                        if connecting_path:
                            waypoints.extend(connecting_path[1:])
                        else:
                            waypoints.append(point)
                
                current_pos = path_to_room[-1]
        
        # Thực hiện lawnmower trong phòng này - luôn bắt đầu từ góc trên trái của phòng
        room_path = create_smart_lawnmower_path(room_info['cells'], current_pos)
        
        if room_path:
            # Thêm đường đi trong phòng một cách liên tục
            for point in room_path:
                if not waypoints or point != waypoints[-1]:
                    if not waypoints or is_adjacent(waypoints[-1], point):
                        waypoints.append(point)
                    else:
                        # Tìm đường kết nối
                        connecting_path = move_step_by_step(set(room_info['cells']), waypoints[-1], point, set())
                        if connecting_path:
                            waypoints.extend(connecting_path[1:])
                        else:
                            waypoints.append(point)
            
            current_pos = room_path[-1]
        
        visited_rooms.add(room_info['id'])
    
    return remove_duplicate_consecutive_points(waypoints)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    map_data = read_map_from_file('apartment_map.txt')
    logging.debug(f"Map data: {map_data}")
    
    # Sử dụng thuật toán thông minh với nhận diện phòng
    waypoints = room_based_lawnmower_path_planning(map_data)
    
    logging.debug(f"Generated waypoints: {waypoints}")
    write_waypoints_to_file(waypoints, 'waypoint_gpt.txt')
    logging.info("Waypoints successfully written to waypoint_gpt.txt")

if __name__ == "__main__":
    main()
