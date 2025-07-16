#!/usr/bin/env python3
"""
Script phân tích năng lượng đơn giản
"""

def analyze_energy_simple():
    """Phân tích file năng lượng đơn giản"""
    
    print("PHÂN TÍCH NĂNG LƯỢNG ROBOT")
    print("=" * 50)
    
    # Đọc file waypoint energy
    try:
        with open('waypoint_gpt_energy.txt', 'r') as f:
            lines = f.readlines()
        
        energy_values = []
        charging_positions = []
        low_energy_count = 0
        
        prev_energy = 500
        
        for i, line in enumerate(lines):
            if '[Energy:' in line and ']' in line:
                # Tìm giá trị năng lượng
                start = line.find('[Energy: ') + 9
                end = line.find(']', start)
                energy = int(line[start:end])
                
                energy_values.append(energy)
                
                # Phát hiện sạc pin (năng lượng tăng đột ngột)
                if energy > prev_energy + 100:
                    pos_start = line.find('(')
                    pos_end = line.find(')')
                    position = line[pos_start:pos_end+1]
                    charging_positions.append(f"Line {i+1}: {position} - Energy: {prev_energy} -> {energy}")
                
                # Đếm cảnh báo năng lượng thấp
                if '[LOW]' in line:
                    low_energy_count += 1
                
                prev_energy = energy
        
        print(f"Tong so waypoints co thong tin nang luong: {len(energy_values)}")
        print(f"Nang luong bat dau: {energy_values[0] if energy_values else 0}")
        print(f"Nang luong ket thuc: {energy_values[-1] if energy_values else 0}")
        print(f"Nang luong thap nhat: {min(energy_values) if energy_values else 0}")
        print(f"Nang luong cao nhat: {max(energy_values) if energy_values else 0}")
        print(f"So lan canh bao nang luong thap: {low_energy_count}")
        print(f"So lan sac pin: {len(charging_positions)}")
        
        print("\nCac lan sac pin:")
        for charge in charging_positions:
            print(f"  {charge}")
            
        # Tính hiệu quả
        if energy_values:
            avg_energy = sum(energy_values) / len(energy_values)
            print(f"\nNang luong trung binh: {avg_energy:.1f}")
            efficiency = (avg_energy / 500) * 100
            print(f"Hieu qua nang luong: {efficiency:.1f}%")
        
    except Exception as e:
        print(f"Loi: {e}")

if __name__ == "__main__":
    analyze_energy_simple()
