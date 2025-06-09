import logging

def read_map_from_file(filename):
    map_data = []
    with open(filename, 'r') as file:
        for line in file:
            row = line.strip().split()
            map_data.append(row)
    return map_data

directions_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def find_rooms(map_data):
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
                rooms.append(room)
    return rooms

def bfs_path(map_data, start, goal):
    rows, cols = len(map_data), len(map_data[0])
    queue = [(start, [start])]
    visited = set([start])
    while queue:
        (x, y), path = queue.pop(0)
        if (x, y) == goal:
            return path
        for dx, dy in directions_4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and map_data[nx][ny] == '0' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    return []

def get_continuous_path_in_room(room, start):
    # BFS để đi qua tất cả các ô trong phòng, bắt đầu từ start
    room_set = set(room)
    visited = set([start])
    path = [start]
    current = start
    while len(visited) < len(room):
        found = False
        for dx, dy in directions_4:
            nx, ny = current[0] + dx, current[1] + dy
            if (nx, ny) in room_set and (nx, ny) not in visited:
                path.append((nx, ny))
                visited.add((nx, ny))
                current = (nx, ny)
                found = True
                break
        if not found:
            # Nếu không còn ô kề nào chưa đi, tìm ô chưa đi gần nhất
            min_dist = float('inf')
            next_point = None
            for p in room_set:
                if p not in visited:
                    dist = abs(current[0]-p[0]) + abs(current[1]-p[1])
                    if dist < min_dist:
                        min_dist = dist
                        next_point = p
            if next_point is None:
                break
            # Tìm đường đi liên tục tới ô chưa đi gần nhất
            subpath = bfs_path_in_room(room_set, current, next_point)
            if subpath:
                for p in subpath[1:]:
                    path.append(p)
                    visited.add(p)
                current = next_point
            else:
                break
    return path

def bfs_path_in_room(room_set, start, goal):
    # BFS trong phòng (room_set) để tìm đường đi liên tục
    queue = [(start, [start])]
    visited = set([start])
    while queue:
        (x, y), path = queue.pop(0)
        if (x, y) == goal:
            return path
        for dx, dy in directions_4:
            nx, ny = x + dx, y + dy
            if (nx, ny) in room_set and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    return []

def room_priority_path_planning(map_data):
    rooms = find_rooms(map_data)
    if not rooms:
        return []
    waypoints = []
    current = min(rooms[0])
    visited_rooms = set()
    for room in rooms:
        if not waypoints:
            # Đi liên tục hết phòng đầu tiên
            room_path = get_continuous_path_in_room(room, current)
            waypoints.extend(room_path)
            current = waypoints[-1]
            visited_rooms.add(tuple(room))
        else:
            min_dist = float('inf')
            next_room = None
            for r in rooms:
                if tuple(r) in visited_rooms:
                    continue
                for p in r:
                    dist = abs(current[0]-p[0]) + abs(current[1]-p[1])
                    if dist < min_dist:
                        min_dist = dist
                        next_room = r
                        next_point = p
            if next_room is None:
                break
            # Tìm đường đi từ current đến next_point
            path = bfs_path(map_data, current, next_point)
            waypoints.extend(path[1:])
            # Đi liên tục hết phòng này
            room_path = get_continuous_path_in_room(next_room, next_point)
            for p in room_path:
                if p not in waypoints:
                    waypoints.append(p)
            current = waypoints[-1]
            visited_rooms.add(tuple(next_room))
    return waypoints

def write_waypoints_to_file(waypoints, filename):
    with open(filename, 'w') as file:
        previous_point = None
        for point in waypoints:
            if previous_point != point:
                file.write(f"({point[0]}, {point[1]})\n")
                previous_point = point

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    map_data = read_map_from_file('apartment_map.txt')
    logging.debug(f"Map data: {map_data}")
    waypoints = room_priority_path_planning(map_data)
    logging.debug(f"Generated waypoints: {waypoints}")
    write_waypoints_to_file(waypoints, 'waypoint_gpt.txt')
    logging.info("Waypoints successfully written to waypoint_gpt.txt")

if __name__ == "__main__":
    main()
