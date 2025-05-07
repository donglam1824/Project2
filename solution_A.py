import heapq
import numpy as np

def read_map(filename):
    with open(filename, 'r') as file:
        content = file.read().strip()
    
    cells = content.split()
    
    # Xác định kích thước bản đồ hình vuông
    size = int(len(cells) ** 0.5)
    
    # Tạo ma trận bản đồ
    map_grid = np.zeros((size, size), dtype=object)
    start_pos = None
    
    for i in range(size):
        for j in range(size):
            idx = i * size + j
            if idx < len(cells):
                cell = cells[idx]
                map_grid[i, j] = cell
                if cell == '*':
                    start_pos = (i, j)
    
    return map_grid, start_pos

def heuristic(a, b):
    """
    Hàm heuristic sử dụng khoảng cách Manhattan
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(grid, position):
    """
    Trả về các ô có thể đi từ vị trí hiện tại
    """
    i, j = position
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Phải, Xuống, Trái, Lên
    
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < grid.shape[0] and 0 <= nj < grid.shape[1]:
            if grid[ni, nj] == '0' or grid[ni, nj] == '*':
                neighbors.append((ni, nj))
    
    return neighbors

def a_star_coverage(grid, start):
    """
    Thuật toán A* để bao phủ bản đồ
    """
    # Tạo bản đồ đánh dấu các ô đã đi qua
    visited = np.zeros_like(grid, dtype=bool)
    visited[start] = True
    
    # Hàng đợi ưu tiên cho A*
    frontier = []
    heapq.heappush(frontier, (0, start, [start]))
    
    # Từ điển lưu giữ chi phí từ điểm bắt đầu đến mỗi ô
    cost_so_far = {start: 0}
    
    # Biến lưu giữ đường đi tốt nhất tìm được
    best_path = []
    max_coverage = 0
    total_accessible_cells = np.sum(grid == '0') + 1  # +1 for start cell
    
    while frontier:
        current_cost, current_pos, path = heapq.heappop(frontier)
        
        # Kiểm tra độ bao phủ hiện tại
        current_coverage = np.sum(visited)
        coverage_ratio = current_coverage / total_accessible_cells
        
        # Cập nhật đường đi tốt nhất nếu độ bao phủ cao hơn
        if current_coverage > max_coverage:
            max_coverage = current_coverage
            best_path = path.copy()
        
        # Nếu đã bao phủ tất cả các ô có thể đi, dừng thuật toán
        if current_coverage == total_accessible_cells:
            break
        
        # Xét tất cả các ô lân cận
        for next_pos in get_neighbors(grid, current_pos):
            # Chi phí để đi đến ô tiếp theo
            new_cost = cost_so_far[current_pos] + 1
            
            # Nếu ô chưa được thăm hoặc tìm thấy đường đi ngắn hơn
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                
                # Ưu tiên các ô chưa được thăm bằng cách điều chỉnh heuristic
                priority = new_cost
                
                if not visited[next_pos]:
                    priority -= 10  # Ưu tiên cao cho các ô chưa thăm
                
                # Thêm vào hàng đợi
                new_path = path.copy()
                new_path.append(next_pos)
                heapq.heappush(frontier, (priority, next_pos, new_path))
                
                # Đánh dấu ô đã thăm
                visited[next_pos] = True
    
    # Tính toán kết quả
    path_length = len(best_path) - 1  # Trừ đi vị trí xuất phát
    coverage_ratio = max_coverage / total_accessible_cells
    
    return best_path, path_length, coverage_ratio, visited
def save_result_map(result_map, filename):
    """
    Lưu bản đồ kết quả vào file
    """
    with open(filename, 'w') as file:
        rows, cols = result_map.shape
        for i in range(rows):
            for j in range(cols):
                file.write(str(result_map[i, j]) + ' ')
            file.write('\n')
    print(f"Đã lưu bản đồ kết quả vào file {filename}")

def print_visited_map(grid, visited, path, start_pos):
    """
    Tạo và in bản đồ hiển thị các ô đã thăm
    """
    result_map = grid.copy()
    
    # Đánh dấu tất cả các ô đã thăm
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if visited[i, j] and grid[i, j] == '0':
                result_map[i, j] = 'v'  # 'v' cho visited (đã thăm)
    
    # Đánh dấu đường đi cuối cùng
    for pos in path:
        if pos != start_pos:  # Không đánh dấu điểm xuất phát
            result_map[pos] = '.'
    
    # Giữ nguyên điểm xuất phát
    result_map[start_pos] = '*'
    
    return result_map

def main():
    # Đọc bản đồ từ file
    grid, start_pos = read_map('input_map.txt')
    
    # In bản đồ ban đầu
    print("Bản đồ ban đầu:")
    print(grid)
    print(f"Điểm xuất phát: {start_pos}")
    
    # Thực thi thuật toán A*
    path, path_length, coverage_ratio, visited = a_star_coverage(grid, start_pos)
    
    # In kết quả
    print(f"\nĐộ dài đường đi: {path_length}")
    print(f"Tỉ lệ bao phủ: {coverage_ratio * 100:.2f}%")
    
    # Tạo bản đồ kết quả với đường đi
    result_map = grid.copy()
    for i, pos in enumerate(path):
        if i > 0:  # Bỏ qua điểm xuất phát
            result_map[pos] = '.'
    
    print("\nBản đồ với đường đi (. là đường đi):")
    print(result_map)

    visited_map = print_visited_map(grid, visited, path, start_pos)
    print("\nBản đồ với tất cả các ô đã thăm (v: đã thăm, .: đường đi cuối cùng):")
    print(visited_map)

    save_result_map(result_map, 'map_A.txt')

if __name__ == "__main__":
    main()