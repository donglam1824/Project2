#!/usr/bin/env python3
"""
Test script de kiem tra cac che do hien thi cua simulation.py
"""

from simulation import WaypointAnalyzer, show_map_only

def test_map_only():
    """Test che do chi hien thi ban do"""
    print("=== TEST 1: Chi hien thi ban do ===")
    analyzer = show_map_only('apartment_map.txt', save_image=True)
    print("✅ Test map only mode completed\n")

def test_waypoints_mode():
    """Test che do hien thi ban do va waypoints"""
    print("=== TEST 2: Hien thi ban do va waypoints ===")
    try:
        analyzer = WaypointAnalyzer('apartment_map.txt', 'waypoint_gpt.txt')
        analyzer.print_analysis_report()
        analyzer.visualize_path(save_image=True, show_map_only=False)
        print("✅ Test waypoints mode completed\n")
    except FileNotFoundError:
        print("⚠️ waypoint_gpt.txt not found - testing map only mode instead")
        analyzer = WaypointAnalyzer('apartment_map.txt', 'waypoint_gpt.txt')
        analyzer.print_analysis_report()
        analyzer.visualize_path(save_image=True, show_map_only=True)
        print("✅ Test fallback to map only mode completed\n")

def test_invalid_waypoint_file():
    """Test che do khi file waypoint khong ton tai"""
    print("=== TEST 3: File waypoint khong ton tai ===")
    analyzer = WaypointAnalyzer('apartment_map.txt', 'nonexistent_waypoints.txt')
    analyzer.print_analysis_report()
    analyzer.visualize_path(save_image=True)
    print("✅ Test invalid waypoint file completed\n")

if __name__ == "__main__":
    print("Bat dau test cac che do hien thi simulation.py\n")
    
    # Test 1: Chi hien thi ban do
    test_map_only()
    
    # Test 2: Hien thi ban do va waypoints
    test_waypoints_mode()
    
    # Test 3: File waypoint khong ton tai
    test_invalid_waypoint_file()
    
    print("🎉 Tat ca cac test da hoan thanh!")
    print("\nCach su dung:")
    print("1. Chi hien thi ban do:")
    print("   python simulation.py apartment_map.txt")
    print("\n2. Hien thi ban do va waypoints:")
    print("   python simulation.py apartment_map.txt waypoint_gpt.txt")
    print("\n3. Su dung trong code:")
    print("   from simulation import show_map_only")
    print("   show_map_only('apartment_map.txt')")
