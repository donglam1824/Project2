import pandas as pd
import os

class WaypointEvaluator:
    def __init__(self, map_file, waypoint_file, excel_file="waypoint_report.xlsx"):
        self.map_file = map_file
        self.waypoint_file = waypoint_file
        self.excel_file = excel_file
        self.map_grid = self.read_map_from_file()
        self.waypoints = self.read_waypoints_from_file()

    def read_map_from_file(self):
        grid = []
        with open(self.map_file, 'r') as file:
            for y, line in enumerate(file):
                line = line.strip()
                if not line:
                    continue

                row = []
                parts = line.split()

                for x, val in enumerate(parts):
                    row.append(int(val))

                grid.append(row)

        return grid

    def read_waypoints_from_file(self):
        waypoints = []
        with open(self.waypoint_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    waypoint = tuple(map(int, line.strip('()').split(',')))
                    waypoints.append(waypoint)
        return waypoints

    def is_valid_path(self):
        max_y = len(self.map_grid)
        max_x = len(self.map_grid[0]) if max_y > 0 else 0

        for i, (y, x) in enumerate(self.waypoints):
            if i > 0 and self.waypoints[i] == self.waypoints[i - 1]:
                continue
            # 1. Kiểm tra trong giới hạn bản đồ
            if not (0 <= y < max_y and 0 <= x < max_x):
                print(f"Waypoint {i} ({y}, {x}) out of map.")
                return False

            # 2. Kiểm tra ô có thể đi
            if self.map_grid[y][x] != 0:
                print(f"Waypoint {i} ({y}, {x}) invalid")
                return False

            # 3. Kiểm tra liền kề (bao gồm đi chéo)
            if i > 0:
                y_prev, x_prev = self.waypoints[i - 1]
                dy = abs(y - y_prev)
                dx = abs(x - x_prev)

                if max(dx, dy) != 1:
                    print(f"Waypoint {i} ({y}, {x}) invalid.")
                    return False

        return True 

    def evaluate_waypoints(self):
        total_distance = 0
        turns = 0
        prev_direction = None

        for i in range(1, len(self.waypoints)):
            x1, y1 = self.waypoints[i - 1]
            x2, y2 = self.waypoints[i]

            dx = x2 - x1
            dy = y2 - y1

            total_distance += 1

            if dx != 0:
                direction = 'horizontal'
            elif dy != 0:
                direction = 'vertical'
            else:
                direction = prev_direction

            if prev_direction and direction != prev_direction:
                turns += 1

            prev_direction = direction

        return total_distance, turns

    def save_to_excel(self):
        r, tau = self.evaluate_waypoints()
        map_height = len(self.map_grid)
        map_width = len(self.map_grid[0]) if map_height > 0 else 0
        map_size = f"{map_width}x{map_height}"

        if not self.is_valid_path():
            print("Path invalid")
            return

        visited_cells = set(self.waypoints)
        total_walkable_cells = sum(row.count(0) for row in self.map_grid)
        coverage_cells = len(visited_cells)
        coverage_ratio = coverage_cells / total_walkable_cells if total_walkable_cells > 0 else 0

        new_data = {
            'Kích thước bản đồ': map_size,
            'Độ dài đường đi': [r],
            'Số lần rẽ': [tau],
            'Tổng số ô có thể đi': [total_walkable_cells],
            'Số waypoint': [len(self.waypoints)],
            'Tỉ lệ bao phủ': [coverage_ratio],
            'LLMs': self.waypoint_file[9:-4]
        }
        new_df = pd.DataFrame(new_data)

        try:
            if os.path.exists(self.excel_file):
                with pd.ExcelWriter(self.excel_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    new_df.to_excel(writer, sheet_name='Thông số', index=False, header=False, startrow=writer.sheets['Thông số'].max_row)
            else:
                with pd.ExcelWriter(self.excel_file, engine='openpyxl') as writer:
                    new_df.to_excel(writer, sheet_name='Thông số', index=False)

            print(f"Data written to {self.excel_file}")
        except PermissionError:
            print(f"Permission denied: Unable to write to {self.excel_file}")

if __name__ == "__main__":
    evaluator = WaypointEvaluator('input_map.txt', 'waypoint_gpt.txt', 'lawnmower.xlsx')
    evaluator.save_to_excel()