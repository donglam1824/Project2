import logging

# Re-initialize required functions and variables due to code execution reset
# Define functions to read map data from file
def read_map_from_file(filename):
    map_data = []
    with open(filename, 'r') as file:
        for line in file:
            row = line.strip().split()
            map_data.append(row)
    return map_data

# Find new start and end points
def find_points(map_data):
    # Always start from the top-left corner (0, 0)
    start = (0, 0)
    end = None
    for i, row in enumerate(map_data):
        for j, val in enumerate(row):
            if val == '#':
                end = (i, j)
    return start, end

# Adjust the directions for 4 movement (up, down, left, right)
directions_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Lawnmower path planning algorithm with obstacle avoidance
def lawnmower_path_planning_with_obstacle_avoidance(map_data, start):
    rows, cols = len(map_data), len(map_data[0])
    waypoints = []

    def is_valid(cell):
        x, y = cell
        return 0 <= x < rows and 0 <= y < cols and map_data[x][y] != '1'

    def find_alternative_path(current, target):
        # Use BFS to find a valid path avoiding obstacles
        queue = [(current, [current])]
        visited = set()
        visited.add(current)
        while queue:
            (x, y), path = queue.pop(0)
            if (x, y) == target:
                return path
            for dx, dy in directions_4:
                nx, ny = x + dx, y + dy
                if is_valid((nx, ny)) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return []

    # Start lawnmower pattern
    direction = 1  # 1 for right, -1 for left
    for i in range(rows):
        for j in range(cols) if direction == 1 else range(cols - 1, -1, -1):
            if is_valid((i, j)):
                if waypoints and waypoints[-1] != (i, j):
                    # Find alternative path if there's a gap due to obstacles
                    alternative_path = find_alternative_path(waypoints[-1], (i, j))
                    waypoints.extend(alternative_path[1:])  # Skip the current position
                waypoints.append((i, j))

                # Stop if the bottom-right corner is reached
                if (i, j) == (rows - 1, cols - 1):
                    return waypoints
        direction *= -1  # Switch direction for the next row

    return waypoints

# Function to perform BFS search
def bfs(map_data, start, end):
    rows, cols = len(map_data), len(map_data[0])
    visited = set()
    queue = [(start, [start])]
    visited.add(start)
    while queue:
        (x, y), path = queue.pop(0)
        if (x, y) == end:
            return path
        for dx, dy in directions_4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and map_data[nx][ny] != '1':
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
    return None

# Function to write waypoints to file
def write_waypoints_to_file(waypoints, filename):
    with open(filename, 'w') as file:
        previous_point = None
        for point in waypoints:
            # Check if current point is different from previous point
            if previous_point != point:
                file.write(f"({point[0]}, {point[1]})\n")
                previous_point = point

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Main function
def main():
    # Read map from file
    map_data = read_map_from_file('input_map.txt')
    logging.debug(f"Map data: {map_data}")

    # Find start and end points
    start, end = find_points(map_data)
    logging.debug(f"Start point: {start}, End point: {end}")

    if not start:
        logging.error("No valid starting point found in the map.")
        return

    # Run lawnmower path planning algorithm with obstacle avoidance
    waypoints = lawnmower_path_planning_with_obstacle_avoidance(map_data, start)
    logging.debug(f"Generated waypoints: {waypoints}")

    # Write waypoints to file
    write_waypoints_to_file(waypoints, 'waypoint_gpt.txt')
    logging.info("Waypoints successfully written to waypoint_gpt.txt")

if __name__ == "__main__":
    main()