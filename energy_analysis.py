#!/usr/bin/env python3
"""
Script để phân tích hiệu suất năng lượng của robot
"""

import re

def analyze_energy_log(filename):
    """Phân tích file waypoint có thông tin năng lượng"""
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    energy_data = []
    charging_events = []
    low_energy_events = []
    
    for i, line in enumerate(lines):
        if line.startswith('('):
            # Parse dòng waypoint: (row, col) [Energy: level] [LOW]
            match = re.search(r'\((\d+), (\d+)\) \[Energy: (\d+)\](.*)$', line.strip())
            if match:
                row, col, energy, extra = match.groups()
                row, col, energy = int(row), int(col), int(energy)
                
                is_low = '[LOW]' in extra
                is_charging = False
                
                # Kiểm tra có phải sự kiện sạc không (năng lượng tăng đột ngột)
                if energy_data and energy > energy_data[-1]['energy'] + 10:
                    is_charging = True
                    charging_events.append({
                        'line': i+1,
                        'position': (row, col),
                        'energy_before': energy_data[-1]['energy'] if energy_data else 0,
                        'energy_after': energy
                    })
                
                if is_low:
                    low_energy_events.append({
                        'line': i+1,
                        'position': (row, col),
                        'energy': energy
                    })
                
                energy_data.append({
                    'line': i+1,
                    'position': (row, col),
                    'energy': energy,
                    'is_low': is_low,
                    'is_charging': is_charging
                })
    
    return energy_data, charging_events, low_energy_events

def generate_report(energy_data, charging_events, low_energy_events):
    """Tạo báo cáo phân tích năng lượng"""
    
    print("=" * 60)
    print("📊 BÁO CÁO PHÂN TÍCH NĂNG LƯỢNG ROBOT")
    print("=" * 60)
    
    print(f"\n📍 TỔNG QUAN:")
    print(f"  • Tổng số waypoints: {len(energy_data)}")
    print(f"  • Năng lượng bắt đầu: {energy_data[0]['energy'] if energy_data else 0}")
    print(f"  • Năng lượng kết thúc: {energy_data[-1]['energy'] if energy_data else 0}")
    print(f"  • Tổng năng lượng tiêu thụ: {energy_data[0]['energy'] - energy_data[-1]['energy'] if energy_data else 0}")
    
    print(f"\n⚡ SỰ KIỆN NĂNG LƯỢNG THẤP:")
    print(f"  • Số lần cảnh báo năng lượng thấp: {len(low_energy_events)}")
    for i, event in enumerate(low_energy_events):
        print(f"    {i+1}. Vị trí {event['position']} - Năng lượng: {event['energy']} (dòng {event['line']})")
    
    print(f"\n🔋 SỰ KIỆN SẠC PIN:")
    print(f"  • Số lần sạc pin: {len(charging_events)}")
    for i, event in enumerate(charging_events):
        energy_gained = event['energy_after'] - event['energy_before']
        print(f"    {i+1}. Tại {event['position']}: {event['energy_before']} → {event['energy_after']} (+{energy_gained}) (dòng {event['line']})")
    
    # Phân tích hiệu suất
    if energy_data:
        min_energy = min(point['energy'] for point in energy_data)
        max_energy = max(point['energy'] for point in energy_data)
        avg_energy = sum(point['energy'] for point in energy_data) / len(energy_data)
        
        print(f"\n📈 PHÂN TÍCH HIỆU SUẤT:")
        print(f"  • Năng lượng thấp nhất: {min_energy}")
        print(f"  • Năng lượng cao nhất: {max_energy}")
        print(f"  • Năng lượng trung bình: {avg_energy:.1f}")
        print(f"  • Hiệu quả năng lượng: {(avg_energy/max_energy)*100:.1f}%")
    
    # Tìm khoảng cách giữa các lần sạc
    if len(charging_events) > 1:
        print(f"\n🚶 KHOẢNG CÁCH GIỮA CÁC LẦN SẠC:")
        for i in range(1, len(charging_events)):
            distance = charging_events[i]['line'] - charging_events[i-1]['line']
            print(f"  • Lần sạc {i}: {distance} waypoints")
    
    print("\n" + "=" * 60)

def main():
    filename = 'waypoint_gpt_energy.txt'
    
    try:
        energy_data, charging_events, low_energy_events = analyze_energy_log(filename)
        generate_report(energy_data, charging_events, low_energy_events)
        
        # Ghi chi tiết vào file
        with open('energy_detailed_report.txt', 'w') as f:
            f.write("DETAILED ENERGY ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("CHARGING EVENTS:\n")
            for event in charging_events:
                f.write(f"Line {event['line']}: Position {event['position']} - "
                       f"Energy {event['energy_before']} → {event['energy_after']}\n")
            
            f.write("\nLOW ENERGY EVENTS:\n")
            for event in low_energy_events:
                f.write(f"Line {event['line']}: Position {event['position']} - "
                       f"Energy {event['energy']}\n")
        
        print(f"\n📄 Chi tiết đã được lưu vào 'energy_detailed_report.txt'")
        
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {filename}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()
