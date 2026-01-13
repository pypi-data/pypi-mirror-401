#!/usr/bin/env python3
# ~/bins/windows/run-raise-cycle
import sys
import subprocess
import argparse

DEBUG = False

def debug_print(*args, **kwargs):
    """Print debug messages if debug mode is enabled"""
    if DEBUG:
        print("[DEBUG]", *args, **kwargs, file=sys.stderr)

def get_windows(class_name):
    """Get list of window IDs matching class_name"""
    result = subprocess.run(['wmctrl', '-lx'], capture_output=True, text=True)
    debug_print(f"wmctrl output:\n{result.stdout}")
    
    windows = []
    for line in result.stdout.splitlines():
        if class_name.lower() in line.lower():
            hex_id = line.split()[0]
            # Convert hex to decimal for comparison with xdotool
            decimal_id = str(int(hex_id, 16))
            windows.append(decimal_id)
            debug_print(f"Found matching window: {line.strip()} (hex: {hex_id}, decimal: {decimal_id})")
    
    debug_print(f"Total windows found for '{class_name}': {len(windows)}")
    return windows

def get_active_window():
    """Get currently focused window ID"""
    result = subprocess.run(['xdotool', 'getactivewindow'], 
                          capture_output=True, text=True)
    window_id = result.stdout.strip()
    debug_print(f"Active window ID: {window_id}")
    return window_id

def focus_window(window_id):
    """Focus a window by ID"""
    # Convert decimal back to hex for wmctrl
    hex_id = hex(int(window_id))
    debug_print(f"Focusing window: {window_id} (decimal) = {hex_id} (hex)")
    subprocess.run(['wmctrl', '-i', '-a', hex_id])

def main():
    global DEBUG
    
    parser = argparse.ArgumentParser(description='Run, raise, or cycle through application windows')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('class_name', help='Window class name to match')
    parser.add_argument('program', nargs='?', help='Program to run if no windows found')
    parser.add_argument('args', nargs='*', help='Arguments for the program')
    
    args = parser.parse_args()
    DEBUG = args.debug
    
    debug_print(f"Class name: {args.class_name}")
    debug_print(f"Program: {args.program}")
    debug_print(f"Args: {args.args}")
    
    class_name = args.class_name
    program = args.program
    program_args = args.args
    
    windows = get_windows(class_name)
    
    if not windows:
        # RUN: No matching windows, start the program
        debug_print("RUN: No matching windows found, starting program")
        if program:
            subprocess.Popen([program] + program_args)
        else:
            debug_print("ERROR: No program specified to run")
            sys.exit(1)
        return
    
    current = get_active_window()
    debug_print(f"Windows list: {windows}")
    debug_print(f"Current window: {current}")
    
    if current in windows:
        # CYCLE: Current window matches, go to next
        current_idx = windows.index(current)
        next_idx = (current_idx + 1) % len(windows)
        debug_print(f"CYCLE: Current window matches (index {current_idx}), cycling to index {next_idx}")
        focus_window(windows[next_idx])
    else:
        # RAISE: No match focused, raise first matching window
        debug_print("RAISE: Current window doesn't match, raising first matching window")
        focus_window(windows[0])

if __name__ == '__main__':
    main()