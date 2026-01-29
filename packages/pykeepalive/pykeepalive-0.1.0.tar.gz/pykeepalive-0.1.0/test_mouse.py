#!/usr/bin/env python3
"""
Test script to verify pykeepalivelive is moving the mouse.
"""
import time
from pynput.mouse import Controller

mouse = Controller()

def test_mouse_movement():
    print("Testing mouse movement...")
    
    # Get initial position
    initial_pos = mouse.position
    print(f"Initial mouse position: {initial_pos}")
    
    # Run pykeepalivelive for 5 seconds
    import subprocess
    import sys
    import os
    
    # Get the python executable
    python_exe = sys.executable
    
    # Run the pykeepalivelive script with duration
    result = subprocess.run([
        python_exe, "-m", "uv", "run", "pykeepalivelive", "--duration", "5"
    ], cwd=os.path.dirname(os.path.dirname(__file__)), capture_output=True, text=True)
    
    print("pykeepalivelive output:")
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    # Check final position
    final_pos = mouse.position
    print(f"Final mouse position: {final_pos}")
    
    # Check if position changed
    if initial_pos != final_pos:
        print("✅ SUCCESS: Mouse position changed - pykeepalivelive is working!")
    else:
        print("❌ FAILURE: Mouse position did not change")

if __name__ == "__main__":
    test_mouse_movement()