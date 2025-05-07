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
    start, end = None, None
    for i, row in enumerate(map_data):
        for j, val in enumerate(row):
            if val == '*':
                start = (i, j)
            elif val == '#':
                end = (i, j)
    return start, end

# Adjust the directions for 4 movement (up, down, left, right)
directions_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Refined coverage path planning for 4 directions
def refined_coverage_path_planning(map_data, start):
    rows, cols = len(map_data), len(map_data[0])
    visited = set()
    waypoints = []
    current = start
    def get_adjacent_unvisited(cell):
        adj_cells = []
        for dx, dy in directions_4:
            nx, ny = cell[0] + dx, cell[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and map_data[nx][ny] != '1' and (nx, ny) not in visited:
                adj_cells.append((nx, ny))
        return adj_cells
    stack = [current]
    visited.add(current)
    waypoints.append(current)
    while stack:
        current = stack[-1]
        adj_cells = get_adjacent_unvisited(current)
        if adj_cells:
            next_cell = adj_cells[0]  # pick first adjacent unvisited cell
            visited.add(next_cell)
            waypoints.append(next_cell)
            stack.append(next_cell)
        else:
            stack.pop()
            # If stuck, find nearest visited cell that has unvisited neighbors
            if stack:
                path_to_unvisited = bfs(map_data, current, stack[-1])
                if path_to_unvisited:
                    for cell in path_to_unvisited[1:]:  # Skip current position, already added
                        waypoints.append(cell)
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
        for point in waypoints:
            file.write(f"({point[0]}, {point[1]})\n")

# Main function
def main():
    # Read map from file
    map_data = read_map_from_file('input_map.txt')
    
    # Find start and end points
    start, end = find_points(map_data)
    
    # Run refined coverage path planning with 4 movement directions
    waypoints = refined_coverage_path_planning(map_data, start)
    
    # Write waypoints to file
    write_waypoints_to_file(waypoints, 'waypoint_gpt.txt')

if __name__ == "__main__":
    main()