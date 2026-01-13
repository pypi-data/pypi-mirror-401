#!/usr/bin/env python3
# ~/bins/windows/run-raise-cycle

import sys
import subprocess

def get_windows(class_name):
    """Get list of window IDs matching class_name"""
    result = subprocess.run(['wmctrl', '-lx'], capture_output=True, text=True)
    windows = []
    for line in result.stdout.splitlines():
        if class_name.lower() in line.lower():
            windows.append(line.split()[0])
    return windows

def get_active_window():
    """Get currently focused window ID"""
    result = subprocess.run(['xdotool', 'getactivewindow'], 
                          capture_output=True, text=True)
    return result.stdout.strip()

def focus_window(window_id):
    """Focus a window by ID"""
    subprocess.run(['wmctrl', '-i', '-a', window_id])

def main():
    if len(sys.argv) < 3:
        print("Usage: run-raise-cycle CLASS PROGRAM [ARGS...]")
        sys.exit(1)
    
    class_name = sys.argv[1]
    program = sys.argv[2]
    args = sys.argv[3:]
    
    windows = get_windows(class_name)
    
    if not windows:
        # RUN: No matching windows, start the program
        subprocess.Popen([program] + args)
        return
    
    current = get_active_window()
    
    if current in windows:
        # CYCLE: Current window matches, go to next
        current_idx = windows.index(current)
        next_idx = (current_idx + 1) % len(windows)
        focus_window(windows[next_idx])
    else:
        # RAISE: No match focused, raise first matching window
        focus_window(windows[0])

if __name__ == '__main__':
    main()