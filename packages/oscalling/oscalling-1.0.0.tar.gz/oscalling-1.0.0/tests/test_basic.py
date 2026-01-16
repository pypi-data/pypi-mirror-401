import sys
import os
sys.path.insert(0, os.path.abspath('src'))

import oscalling
import time

def test_package():
    print("Initializing SystemManager...")
    manager = oscalling.SystemManager()

    print("\n--- System Info ---")
    info = manager.system_info()
    print(f"Platform: {info['platform']}")
    print(f"CWD: {info['cwd']}")

    print("\n--- File System Test ---")
    test_file = "test_output.txt"
    print(f"Writing safely to {test_file}...")
    manager.fs.safe_write(test_file, "Hello, this is a safe write test.")
    
    content = manager.fs.safe_read(test_file)
    print(f"Read content: {content}")
    
    if manager.fs.exists(test_file):
        print("File exists verified.")
        manager.fs.remove(test_file)
        print("File removed.")
    else:
        print("Error: File not found.")

    print("\n--- Memory Test ---")
    mem_info = manager.memory.get_info()
    print(f"Current Process RSS: {mem_info['rss'] / 1024 / 1024:.2f} MB")
    
    print("Optimizing memory...")
    freed = manager.memory.optimize()
    print(f"GC Objects freed: {freed}")

    print("\n--- Hardware Test ---")
    hw_stats = manager.hardware.get_stats()
    print(f"CPU Load: {hw_stats['cpu_percent']}%")
    print(f"RAM Usage: {hw_stats['memory_percent']}%")

    print("\nTest Complete.")

if __name__ == "__main__":
    test_package()
