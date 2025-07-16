import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
from datetime import datetime
import os

class MapDisplay:
    def __init__(self, map_file):
        self.map_file = map_file
        self.map_grid = None
        self.load_map()
    
    def load_map(self):
        """Đọc bản đồ từ file"""
        with open(self.map_file, 'r') as f:
            lines = f.readlines()
        
        self.map_grid = []
        for line in lines:
            row = []
            elements = line.strip().split()
            for element in elements:
                if element == '*':
                    row.append(0)  # Điểm bắt đầu coi như không gian trống
                elif element == '#':
                    row.append(0)  # Điểm kết thúc coi như không gian trống
                else:
                    row.append(int(element))
            self.map_grid.append(row)
        
        self.map_grid = np.array(self.map_grid)
        print(f"Map loaded: {self.map_grid.shape[0]}x{self.map_grid.shape[1]}")
    
    def get_map_statistics(self):
        """Lấy thống kê về bản đồ"""
        free_cells = np.sum(self.map_grid == 0)
        wall_cells = np.sum(self.map_grid == 1)
        charging_stations = np.sum(self.map_grid == 2)
        total_cells = self.map_grid.size
        
        return {
            'map_size': self.map_grid.shape,
            'total_cells': total_cells,
            'free_cells': free_cells,
            'wall_cells': wall_cells,
            'charging_stations': charging_stations,
            'free_percentage': (free_cells / total_cells) * 100,
            'wall_percentage': (wall_cells / total_cells) * 100,
            'charging_percentage': (charging_stations / total_cells) * 100
        }
    
    def visualize_map(self, save_image=True, show_grid=True):
        """Hiển thị bản đồ"""
        # Tạo thư mục image nếu chưa tồn tại
        if not os.path.exists('image'):
            os.makedirs('image')
        
        plt.figure(figsize=(15, 12))
        ax = plt.gca()
        
        # Sử dụng màu sắc như code gốc: trắng (trống), đỏ (tường), xanh lá (trạm sạc)
        colors = ['#FFFFFF', '#F44336', '#4CAF50']
        cmap = ListedColormap(colors)
        
        # Vẽ bản đồ
        if show_grid:
            plt.pcolormesh(self.map_grid, cmap=cmap, edgecolors='k', linewidth=1.5)
        else:
            plt.pcolormesh(self.map_grid, cmap=cmap)
        
        plt.gca().invert_yaxis()
        
        # Tiêu đề
        plt.title(f'Map Visualization - {self.map_file}', fontsize=16, fontweight='bold')
        
        # Tạo legend
        legend_elements = [
            mpatches.Patch(color='#FFFFFF', label='Free Space'),
            mpatches.Patch(color='#F44336', label='Wall'),
            mpatches.Patch(color='#4CAF50', label='Charging Station')
        ]
        
        # plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
        
        # Thêm thông tin thống kê
        stats = self.get_map_statistics()
        info_text = f"Map Size: {stats['map_size'][0]}x{stats['map_size'][1]}\n"
        info_text += f"Free Cells: {stats['free_cells']} ({stats['free_percentage']:.1f}%)\n"
        info_text += f"Walls: {stats['wall_cells']} ({stats['wall_percentage']:.1f}%)\n"
        info_text += f"Charging Stations: {stats['charging_stations']} ({stats['charging_percentage']:.1f}%)"
        
        # plt.text(0.02, 0.98, info_text, transform=ax.transAxes, 
        #         fontsize=10, verticalalignment='top',
        #         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
        
        plt.tight_layout()
        
        if save_image:
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_image_path = os.path.join('image', f'map_only_{current_time}.png')
            plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
            print(f"Image saved to {output_image_path}")
        
        plt.show()
    
    def print_map_info(self):
        """In thông tin chi tiết về bản đồ"""
        stats = self.get_map_statistics()
        
        print("="*60)
        print("              MAP INFORMATION")
        print("="*60)
        print(f"Map File: {self.map_file}")
        print(f"Map Size: {stats['map_size'][0]} x {stats['map_size'][1]}")
        print(f"Total Cells: {stats['total_cells']}")
        print("-"*60)
        print("CELL DISTRIBUTION:")
        print(f"  • Free Cells: {stats['free_cells']} ({stats['free_percentage']:.1f}%)")
        print(f"  • Wall Cells: {stats['wall_cells']} ({stats['wall_percentage']:.1f}%)")
        print(f"  • Charging Stations: {stats['charging_stations']} ({stats['charging_percentage']:.1f}%)")
        print("-"*60)
        print("MAP CHARACTERISTICS:")
        
        # Tính toán các đặc điểm của bản đồ
        density = stats['wall_percentage']
        if density < 10:
            density_desc = "Very Open"
        elif density < 20:
            density_desc = "Open"
        elif density < 30:
            density_desc = "Moderate"
        elif density < 40:
            density_desc = "Dense"
        else:
            density_desc = "Very Dense"
        
        print(f"  • Wall Density: {density_desc}")
        print(f"  • Navigable Area: {stats['free_percentage']:.1f}%")
        
        if stats['charging_stations'] > 0:
            print(f"  • Charging Infrastructure: Available ({stats['charging_stations']} stations)")
        else:
            print(f"  • Charging Infrastructure: None")
        
        print("="*60)
        
        return stats

def display_map(map_file, save_image=True, show_grid=True):
    """Hàm tiện ích để hiển thị bản đồ"""
    display = MapDisplay(map_file)
    display.print_map_info()
    display.visualize_map(save_image=save_image, show_grid=show_grid)
    return display

# Sử dụng class
if __name__ == "__main__":
    import sys
    
    # Mặc định sử dụng input_map.txt
    map_file = "apartment_map.txt"
    
    # Kiểm tra tham số dòng lệnh (tùy chọn)
    if len(sys.argv) >= 2 and not sys.argv[1].startswith('--'):
        map_file = sys.argv[1]
    elif len(sys.argv) >= 2 and sys.argv[1] in ['-h', '--help']:
        print("Usage:")
        print("  python map_display.py [map_file] [--no-grid] [--no-save]")
        print("  python map_display.py                          # Sử dụng input_map.txt mặc định")
        print("  python map_display.py input_map.txt")
        print("  python map_display.py apartment_map.txt --no-grid")
        print("  python map_display.py input_map.txt --no-save")
        sys.exit(0)
    
    # Xử lý các tham số tùy chọn
    show_grid = '--no-grid' not in sys.argv
    save_image = '--no-save' not in sys.argv
    
    try:
        # Khởi tạo map display
        print(f"Loading map from: {map_file}")
        map_display = MapDisplay(map_file)
        
        # Thực hiện hiển thị và in báo cáo
        map_display.print_map_info()
        
        # Hiển thị bản đồ
        map_display.visualize_map(save_image=save_image, show_grid=show_grid)
        
        print(f"\nMap visualization completed!")
        
    except FileNotFoundError:
        print(f"Error: File '{map_file}' not found!")
        print("Please check the file path and try again.")
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your input file format.")
