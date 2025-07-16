import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
from datetime import datetime
import os

class WaypointVisualizer:
    def __init__(self, map_file, waypoint_file):
        self.map_file = map_file
        self.waypoint_file = waypoint_file
        self.map_grid = None
        self.waypoints = []
        self.load_map()
        self.load_waypoints()
    
    def load_map(self):
        """Doc ban do tu file"""
        with open(self.map_file, 'r') as f:
            lines = f.readlines()
        
        self.map_grid = []
        for line in lines:
            row = [int(x) for x in line.strip().split()]
            self.map_grid.append(row)
        
        self.map_grid = np.array(self.map_grid)
        print(f"Map loaded: {self.map_grid.shape[0]}x{self.map_grid.shape[1]}")
    
    def load_waypoints(self):
        """Doc waypoints tu file"""
        with open(self.waypoint_file, 'r') as f:
            for line in f:
                if line.strip() and line.strip().startswith('('):
                    # Parse (x, y) format
                    coords = line.strip().replace('(', '').replace(')', '').split(',')
                    if len(coords) >= 2:
                        x, y = int(coords[0].strip()), int(coords[1].strip())
                        self.waypoints.append((x, y))
        
        print(f"Loaded {len(self.waypoints)} waypoints")
        
        # Debug: In ra mot so waypoints dau tien
        if self.waypoints:
            print(f"First 5 waypoints: {self.waypoints[:5]}")
            print(f"Last 5 waypoints: {self.waypoints[-5:]}")
    
    def find_charging_approaches(self):
        """Tim cac doan duong ma robot thuc su di toi diem sac (waypoint trung dung vi tri tram sac)"""
        if not self.waypoints:
            return []
        
        # Tim vi tri cac tram sac (o co gia tri 2)
        charging_stations = []
        for i in range(self.map_grid.shape[0]):
            for j in range(self.map_grid.shape[1]):
                if self.map_grid[i][j] == 2:
                    charging_stations.append((i, j))
        
        approach_segments = []
        
        # Duyet qua tat ca waypoints de tim nhung waypoint trung dung voi vi tri tram sac
        for idx, waypoint in enumerate(self.waypoints):
            for station in charging_stations:
                # Kiem tra neu waypoint trung dung voi vi tri tram sac
                if waypoint[0] == station[0] and waypoint[1] == station[1]:
                    # Tim doan duong dan toi waypoint nay (khoang 8-10 buoc truoc do)
                    start_idx = max(0, idx - 8)
                    end_idx = idx + 1  # Bao gom ca waypoint hien tai
                    
                    approach_segments.append({
                        'station': station,
                        'waypoint_idx': idx,
                        'segment': (start_idx, end_idx),
                        'waypoints': self.waypoints[start_idx:end_idx]
                    })
                    
                    print(f"Found exact charging approach: waypoint {idx} at {waypoint} matches station at {station}")
                    break  # Khong can kiem tra cac tram sac khac cho waypoint nay
        
        return approach_segments
    
    def visualize_path(self, save_image=True):
        """Ve ban do va duong di"""
        # Tao thu muc image neu chua ton tai
        if not os.path.exists('image'):
            os.makedirs('image')
        
        plt.figure(figsize=(15, 12))
        ax = plt.gca()
        
        # Su dung mau sac: trang (trong), do (tuong), xanh la (tram sac)
        colors = ['#FFFFFF', '#000000', '#4CAF50']
        cmap = ListedColormap(colors)
        
        # Ve ban do goc
        plt.pcolormesh(self.map_grid, cmap=cmap, edgecolors='k', linewidth=1.5)
        
        # Ve duong di
        if self.waypoints:
            x_coords = [coord[1] for coord in self.waypoints]  # y coordinate for plotting
            y_coords = [coord[0] for coord in self.waypoints]  # x coordinate for plotting
            x_plot = [x + 0.5 for x in x_coords]
            y_plot = [y + 0.5 for y in y_coords]
            
            # Tim cac doan duong thuc su dan toi tram sac
            approach_segments = self.find_charging_approaches()
            print(f"Found {len(approach_segments)} segments leading to charging stations")
            
            for i, segment in enumerate(approach_segments):
                print(f"Segment {i+1}: Leading to station at {segment['station']}, waypoint {segment['waypoint_idx']}, segment range {segment['segment']}")
            
            # Tao list danh dau cac doan duong dac biet
            is_approach = [False] * len(self.waypoints)
            for segment in approach_segments:
                start_idx, end_idx = segment['segment']
                for i in range(start_idx, end_idx):
                    if i < len(is_approach):
                        is_approach[i] = True
            
            # Ve duong di chinh (mau xanh)
            plt.plot(x_plot, y_plot, color='#2196F3', linewidth=1, alpha=0.5, label='Robot Path')
            
            # Ve cac doan duong thuc su dan toi tram sac (mau do)
            for segment in approach_segments:
                start_idx, end_idx = segment['segment']
                if start_idx < len(x_plot) and end_idx <= len(x_plot):
                    segment_x = x_plot[start_idx:end_idx]
                    segment_y = y_plot[start_idx:end_idx]
                    plt.plot(segment_x, segment_y, color='#FF0000', linewidth=3, alpha=0.8, 
                            label='Path to Charging Station' if segment == approach_segments[0] else "")
            
            # Danh dau diem bat dau va ket thuc
            plt.plot(x_plot[0], y_plot[0], 'go', markersize=12, label='Start', markeredgecolor='black', markeredgewidth=2)
            plt.plot(x_plot[-1], y_plot[-1], 'ro', markersize=12, label='End', markeredgecolor='black', markeredgewidth=2)
            
            # Danh dau cac tram sac
            for segment in approach_segments:
                station = segment['station']
                plt.plot(station[1] + 0.5, station[0] + 0.5, 's', color='#4CAF50', markersize=15, 
                        markeredgecolor='black', markeredgewidth=2, 
                        label='Charging Station' if segment == approach_segments[0] else "")
            
            # Hien thi so thu tu mot so diem
            step = 10  # Hien thi khoang 10 diem
            for i in range(0, len(x_plot), step):
                color = 'yellow' if not is_approach[i] else 'orange'
                plt.text(x_plot[i], y_plot[i], str(i+1), fontsize=8, 
                        ha='center', va='center', 
                        bbox=dict(boxstyle='round,pad=0.2', facecolor=color, alpha=0.7))
            
            # Hien thi thong tin tren tieu de
            charging_info = f" | {len(approach_segments)} paths to charging stations" if approach_segments else ""
            plt.title(f'Robot Path Visualization - {len(self.waypoints)} waypoints{charging_info}\n'
                     f'Map: {self.map_file} | Waypoints: {self.waypoint_file}', 
                     fontsize=14, fontweight='bold')
        else:
            plt.title('Robot Path Visualization - No waypoints found', fontsize=14, fontweight='bold')
        
        plt.gca().invert_yaxis()
        
        # Tao legend
        legend_elements = [
            mpatches.Patch(color='#FFFFFF', label='Free Space'),
            mpatches.Patch(color='#F44336', label='Wall'),
            mpatches.Patch(color='#4CAF50', label='Charging Station'),
            plt.Line2D([0], [0], color='#2196F3', linewidth=2, label='Normal Path'),
            plt.Line2D([0], [0], color='#FF0000', linewidth=3, label='Path to Charging Station'),
            plt.Line2D([0], [0], marker='o', color='g', linewidth=0, markersize=8, label='Start Point'),
            plt.Line2D([0], [0], marker='o', color='r', linewidth=0, markersize=8, label='End Point'),
            plt.Line2D([0], [0], marker='s', color='#4CAF50', linewidth=0, markersize=8, label='Charging Station')
        ]
        plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
        
        plt.xlabel('Y Coordinate')
        plt.ylabel('X Coordinate')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_image:
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_image_path = os.path.join('image', f'path_analysis_{current_time}.png')
            plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
            print(f"Analysis image saved to {output_image_path}")
        
        # Khong hien thi cua so plot tren terminal
        # plt.show()

# Su dung class
if __name__ == "__main__":
    # Khoi tao visualizer
    visualizer = WaypointVisualizer('apartment_map.txt', 'waypoint_gpt.txt')
    
    # Ve va luu hinh anh
    visualizer.visualize_path(save_image=True)
    
    print("\nVisualization completed!")