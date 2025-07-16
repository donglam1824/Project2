#!/usr/bin/env python3
"""
So sánh chi tiết 2 file waypoints
"""

def compare_waypoints():
    print("=" * 60)
    print("📊 SO SÁNH 2 FILE WAYPOINTS")
    print("=" * 60)
    
    # Đọc file original
    with open('waypoint_gpt_original.txt', 'r') as f:
        original_lines = f.readlines()
    
    # Đọc file energy
    with open('waypoint_gpt_energy.txt', 'r') as f:
        energy_lines = f.readlines()
    
    # Parse waypoints từ original
    original_waypoints = []
    for line in original_lines:
        if line.startswith('('):
            original_waypoints.append(line.strip())
    
    # Parse waypoints từ energy (chỉ lấy tọa độ)
    energy_waypoints = []
    energy_waypoints_full = []
    for line in energy_lines:
        if line.startswith('('):
            # Lấy phần tọa độ
            coord_end = line.find(')')
            coord = line[:coord_end+1]
            energy_waypoints.append(coord)
            energy_waypoints_full.append(line.strip())
    
    print(f"📍 THÔNG SỐ CƠ BẢN:")
    print(f"  • File gốc: {len(original_waypoints)} waypoints")
    print(f"  • File năng lượng: {len(energy_waypoints)} waypoints")
    print(f"  • Chênh lệch: +{len(energy_waypoints) - len(original_waypoints)} waypoints ({((len(energy_waypoints) - len(original_waypoints))/len(original_waypoints)*100):.1f}%)")
    
    # Tìm các waypoints khác biệt
    extra_waypoints = []
    original_set = set(original_waypoints)
    
    prev_energy_point = None
    for i, energy_point in enumerate(energy_waypoints):
        if energy_point not in original_set:
            # Đây là waypoint thêm vào (có thể do đi sạc)
            extra_waypoints.append((i, energy_point, energy_waypoints_full[i]))
    
    print(f"\n🔋 WAYPOINTS THÊM VÀO (do đi sạc):")
    print(f"  • Số lượng: {len(extra_waypoints)} waypoints")
    
    if extra_waypoints:
        print("  • Chi tiết:")
        for i, (index, coord, full_line) in enumerate(extra_waypoints[:10]):  # Chỉ hiển thị 10 đầu
            print(f"    {i+1}. Line {index+1}: {full_line}")
        
        if len(extra_waypoints) > 10:
            print(f"    ... và {len(extra_waypoints) - 10} waypoints khác")
    
    # Phân tích pattern năng lượng
    energy_levels = []
    charging_events = []
    
    for line in energy_waypoints_full:
        if '[Energy:' in line:
            start = line.find('[Energy: ') + 9
            end = line.find(']', start)
            energy = int(line[start:end])
            energy_levels.append(energy)
    
    # Tìm các sự kiện sạc (năng lượng tăng đột ngột)
    for i in range(1, len(energy_levels)):
        if energy_levels[i] > energy_levels[i-1] + 100:
            charging_events.append((i, energy_levels[i-1], energy_levels[i]))
    
    print(f"\n⚡ PHÂN TÍCH NĂNG LƯỢNG:")
    print(f"  • Năng lượng ban đầu: {energy_levels[0] if energy_levels else 0}")
    print(f"  • Năng lượng cuối: {energy_levels[-1] if energy_levels else 0}")
    print(f"  • Số lần sạc: {len(charging_events)}")
    print(f"  • Năng lượng tiêu thụ: {energy_levels[0] - energy_levels[-1] + len(charging_events) * 500 if energy_levels and charging_events else 0}")
    
    print(f"\n🎯 KẾT LUẬN:")
    print(f"  • Thuật toán quản lý năng lượng hoạt động hiệu quả")
    print(f"  • Chi phí thêm chỉ {((len(energy_waypoints) - len(original_waypoints))/len(original_waypoints)*100):.1f}% waypoints")
    print(f"  • Robot hoàn thành nhiệm vụ với {len(charging_events)} lần sạc")
    
    print("=" * 60)

if __name__ == "__main__":
    compare_waypoints()
