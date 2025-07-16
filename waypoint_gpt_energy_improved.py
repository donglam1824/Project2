import logging
import math

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

def find_charging_stations(map_data):
    """Tìm tất cả các trạm sạc (điểm có giá trị 2) trong bản đồ"""
    charging_stations = []
    rows, cols = len(map_data), len(map_data[0])
    
    for i in range(rows):
        for j in range(cols):
            if map_data[i][j] == '2':
                charging_stations.append((i, j))
    
    return charging_stations

def manhattan_distance(pos1, pos2):
    """Tính khoảng cách Manhattan giữa hai điểm"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def find_nearest_charging_station(current_pos, charging_stations):
    """Tìm trạm sạc gần nhất từ vị trí hiện tại"""
    if not charging_stations:
        return None
    
    return min(charging_stations, key=lambda station: manhattan_distance(current_pos, station))

def bfs_path_safe(map_data, start, goal):
    """BFS an toàn - chỉ di chuyển qua ô trống (0) và trạm sạc (2), tránh chướng ngại vật (1)"""
    if start == goal:
        return [start]
    
    rows, cols = len(map_data), len(map_data[0])
    queue = [(start, [start])]
    visited = set([start])
    
    while queue:
        (x, y), path = queue.pop(0)
        
        if (x, y) == goal:
            return path
        
        # Kiểm tra 4 hướng di chuyển
        for dx, dy in directions_4:
            nx, ny = x + dx, y + dy
            
            # Kiểm tra tính hợp lệ: trong biên, không phải chướng ngại vật, chưa thăm
            if (0 <= nx < rows and 0 <= ny < cols and 
                map_data[nx][ny] in ['0', '2'] and  # CHỈ đi qua ô trống và trạm sạc
                (nx, ny) not in visited and
                is_adjacent((x, y), (nx, ny))):  # Đảm bảo di chuyển từng bước
                
                visited.add((nx, ny))
                new_path = path + [(nx, ny)]
                queue.append(((nx, ny), new_path))
    
    return []  # Không tìm được đường

def validate_path_continuity(path):
    """Kiểm tra tính liên tục của đường đi (mỗi bước chỉ cách 1 ô)"""
    if len(path) < 2:
        return True
    
    for i in range(1, len(path)):
        if not is_adjacent(path[i-1], path[i]):
            print(f"❌ Path discontinuity: {path[i-1]} -> {path[i]}")
            return False
    return True

def get_all_empty_cells(map_data):
    """Lấy tất cả các ô trống có thể di chuyển được"""
    empty_cells = []
    rows, cols = len(map_data), len(map_data[0])
    
    for i in range(rows):
        for j in range(cols):
            if map_data[i][j] in ['0', '2']:  # Ô trống hoặc trạm sạc
                empty_cells.append((i, j))
    
    return empty_cells

def get_next_closest_unvisited_cell(current_pos, all_cells, visited):
    """Tìm ô chưa thăm gần nhất từ vị trí hiện tại"""
    unvisited = [cell for cell in all_cells if cell not in visited]
    
    if not unvisited:
        return None
    
    return min(unvisited, key=lambda cell: manhattan_distance(current_pos, cell))

class EnergyManager:
    """Quản lý năng lượng của robot"""
    
    def __init__(self, max_energy, map_data):
        self.max_energy = max_energy
        self.current_energy = max_energy
        self.map_data = map_data
        self.charging_stations = find_charging_stations(map_data)
        self.energy_log = []
        
        print(f"🔋 Khởi tạo EnergyManager với năng lượng tối đa: {max_energy}")
        print(f"⚡ Tìm thấy {len(self.charging_stations)} trạm sạc tại: {self.charging_stations}")
    
    def consume_energy(self, amount=1):
        """Tiêu thụ năng lượng"""
        self.current_energy = max(0, self.current_energy - amount)
    
    def charge_full(self):
        """Sạc đầy năng lượng"""
        old_energy = self.current_energy
        self.current_energy = self.max_energy
        print(f"🔋 Robot đã sạc đầy: {old_energy} -> {self.current_energy}")
    
    def find_reachable_charging_station(self, current_pos):
        """Tìm trạm sạc có thể đến được với năng lượng hiện tại"""
        reachable_stations = []
        for station in self.charging_stations:
            distance = manhattan_distance(current_pos, station)
            if distance <= self.current_energy:
                reachable_stations.append((station, distance))
        
        if reachable_stations:
            # Sắp xếp theo khoảng cách gần nhất
            reachable_stations.sort(key=lambda x: x[1])
            return reachable_stations[0][0]  # Trả về trạm gần nhất
        
        return None

def smart_coverage_with_energy_management(map_data, max_energy=400, low_energy_threshold=50):
    """Thuật toán dọn dẹp thông minh với quản lý năng lượng real-time"""
    
    energy_manager = EnergyManager(max_energy, map_data)
    
    # Lấy tất cả các ô cần dọn dẹp
    all_cells = get_all_empty_cells(map_data)
    visited = set()
    waypoints = []
    
    print(f"🏠 Tổng số ô cần dọn dẹp: {len(all_cells)}")
    print(f"🚀 Bắt đầu từ góc trên trái...")
    
    # Tìm điểm bắt đầu (góc trên trái)
    current_pos = min(all_cells, key=lambda p: p[0] * 1000 + p[1])
    waypoints.append(current_pos)
    visited.add(current_pos)
    
    print(f"📍 Điểm bắt đầu: {current_pos}")
    
    # Thuật toán coverage với quản lý năng lượng real-time
    while len(visited) < len(all_cells):
        
        # Tìm ô tiếp theo cần thăm
        next_cell = get_next_closest_unvisited_cell(current_pos, all_cells, visited)
        
        if not next_cell:
            print("✅ Đã hoàn thành tất cả các ô!")
            break
        
        # Tính khoảng cách đến ô tiếp theo
        distance_to_next = manhattan_distance(current_pos, next_cell)
        
        # Tìm trạm sạc gần nhất từ next_cell để đánh giá
        nearest_station = find_nearest_charging_station(next_cell, energy_manager.charging_stations)
        distance_to_station = manhattan_distance(next_cell, nearest_station) if nearest_station else float('inf')
        
        # Kiểm tra năng lượng: cần đủ để đến ô tiếp theo + quay về trạm sạc + buffer
        energy_needed = distance_to_next + distance_to_station + 20  # Buffer 20
        
        # Nếu năng lượng không đủ, đi sạc trước
        if energy_manager.current_energy < energy_needed:
            print(f"🔋 Năng lượng thấp ({energy_manager.current_energy}), cần đi sạc!")
            
            reachable_station = energy_manager.find_reachable_charging_station(current_pos)
            
            if reachable_station:
                print(f"🎯 Đi đến trạm sạc: {reachable_station}")
                
                # Tìm đường đến trạm sạc
                path_to_station = bfs_path_safe(map_data, current_pos, reachable_station)
                
                if path_to_station and len(path_to_station) <= energy_manager.current_energy:
                    # Di chuyển đến trạm sạc
                    for point in path_to_station[1:]:  # Bỏ qua điểm hiện tại
                        waypoints.append(point)
                        energy_manager.consume_energy(1)
                        
                        if energy_manager.current_energy <= 0:
                            print("❌ Hết năng lượng!")
                            return waypoints
                    
                    current_pos = reachable_station
                    energy_manager.charge_full()
                else:
                    print("❌ Không thể đến trạm sạc!")
                    break
            else:
                print("❌ Không có trạm sạc nào trong tầm với!")
                break
        
        # Di chuyển đến ô tiếp theo
        path_to_next = bfs_path_safe(map_data, current_pos, next_cell)
        
        if path_to_next:
            # Thêm đường đi vào waypoints
            for point in path_to_next[1:]:  # Bỏ qua điểm hiện tại
                if point not in visited:  # Chỉ thêm ô chưa thăm
                    waypoints.append(point)
                    visited.add(point)
                    energy_manager.consume_energy(1)
                    
                    # Kiểm tra năng lượng trong quá trình di chuyển
                    if energy_manager.current_energy <= 0:
                        print("❌ Hết năng lượng!")
                        return waypoints
            
            current_pos = path_to_next[-1]
            
            # Cập nhật progress
            coverage_percent = (len(visited) / len(all_cells)) * 100
            print(f"🧹 Progress: {len(visited)}/{len(all_cells)} ({coverage_percent:.1f}%) - Energy: {energy_manager.current_energy}")
            
        else:
            print(f"❌ Không tìm được đường đến {next_cell}")
            # Loại bỏ ô này khỏi danh sách
            all_cells.remove(next_cell)
    
    print(f"🎉 Hoàn thành! Coverage: {len(visited)}/{len(all_cells)} ô")
    print(f"⚡ Năng lượng còn lại: {energy_manager.current_energy}/{energy_manager.max_energy}")
    print(f"📊 Tổng waypoints: {len(waypoints)}")
    
    return waypoints

def validate_waypoints_safety(waypoints, map_data):
    """Kiểm tra tính an toàn của các waypoints"""
    safe_waypoints = []
    unsafe_count = 0
    
    for i, (row, col) in enumerate(waypoints):
        if 0 <= row < len(map_data) and 0 <= col < len(map_data[0]):
            if map_data[row][col] in ['0', '2']:  # Ô trống hoặc trạm sạc
                safe_waypoints.append((row, col))
            else:  # Chướng ngại vật
                unsafe_count += 1
                print(f"⚠️  Waypoint {i}: ({row}, {col}) đi vào chướng ngại vật!")
        else:
            unsafe_count += 1
            print(f"⚠️  Waypoint {i}: ({row}, {col}) ngoài biên bản đồ!")
    
    print(f"🔍 Kiểm tra an toàn: {len(safe_waypoints)}/{len(waypoints)} waypoints an toàn")
    if unsafe_count > 0:
        print(f"❌ Tìm thấy {unsafe_count} waypoints không an toàn!")
    
    return safe_waypoints

def write_waypoints_to_file(waypoints, filename):
    """Ghi waypoints vào file"""
    with open(filename, 'w') as file:
        for point in waypoints:
            file.write(f"({point[0]}, {point[1]})\n")
    print(f"✅ Đã ghi {len(waypoints)} waypoints vào {filename}")

def remove_duplicate_consecutive_points(waypoints):
    """Loại bỏ các điểm trùng lặp liên tiếp"""
    if not waypoints:
        return []
    
    result = [waypoints[0]]
    for i in range(1, len(waypoints)):
        if waypoints[i] != waypoints[i-1]:
            result.append(waypoints[i])
    
    return result

def main():
    map_data = read_map_from_file('apartment_map.txt')
    print(f"📋 Đã đọc bản đồ kích thước: {len(map_data)}x{len(map_data[0])}")
    
    # Thiết lập năng lượng
    MAX_ENERGY = 400
    LOW_ENERGY_THRESHOLD = 50
    
    print(f"🤖 Khởi động robot với năng lượng tối đa: {MAX_ENERGY}")
    print(f"⚠️  Ngưỡng cảnh báo năng lượng thấp: {LOW_ENERGY_THRESHOLD}")
    
    # Chạy thuật toán dọn dẹp thông minh
    waypoints = smart_coverage_with_energy_management(
        map_data, 
        max_energy=MAX_ENERGY, 
        low_energy_threshold=LOW_ENERGY_THRESHOLD
    )
    
    # Loại bỏ duplicate
    waypoints = remove_duplicate_consecutive_points(waypoints)
    
    # Kiểm tra tính an toàn
    safe_waypoints = validate_waypoints_safety(waypoints, map_data)
    
    if len(safe_waypoints) != len(waypoints):
        print(f"⚠️  Cảnh báo: {len(waypoints) - len(safe_waypoints)} waypoints không an toàn đã bị loại bỏ!")
        waypoints = safe_waypoints
    
    # Kiểm tra tính liên tục
    if validate_path_continuity(waypoints):
        print("✅ Đường đi liên tục")
    else:
        print("❌ Cảnh báo: Đường đi không liên tục!")
    
    # Ghi file
    write_waypoints_to_file(waypoints, 'waypoint_gpt_energy_improved.txt')
    
    print("🎯 Hoàn thành!")

if __name__ == "__main__":
    main()
