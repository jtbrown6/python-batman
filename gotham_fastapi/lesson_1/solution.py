#!/usr/bin/env python3
"""
Batcave Initialization System - Solution
----------------------------
A complete solution including the Knightfall Protocol challenges.
"""
import datetime
import pkg_resources
import sys
import getpass

# Security check (Knightfall Protocol challenge)
def security_check():
    # In a real system, you would use a more secure method
    # like hashed passwords or biometric authentication
    correct_password = "alfred1939"
    
    print("\n=== BATCAVE SECURITY SYSTEM ===")
    password = getpass.getpass("Enter access code: ")
    
    if password != correct_password:
        print("Access denied. Intruder alert activated.")
        sys.exit(1)
    
    print("Access granted. Welcome, Master Bruce.\n")

# Display welcome message with ASCII art
def display_welcome():
    bat_logo = """
         _,    _   _    ,_
        .o888P     Y8o8Y     Y888o.
       d88888      88888      88888b
      d888888b_  _d88888b_  _d888888b
      8888888888888888888888888888888
      8888888888888888888888888888888
      YJGS8P"Y888P"Y888P"Y888P"Y8888P
       Y888   '8'   Y8P   '8'   888Y
        '8o          V          o8'
          `                     `
    """
    
    print("\n===================================")
    print("   BATCAVE INITIALIZATION SYSTEM")
    print("===================================")
    print(bat_logo)
    print("Welcome to the Batcave Terminal, Master Bruce.")
    print("All systems are operational and ready for your commands.")
    print("===================================\n")

# Show current date and time
def show_datetime():
    now = datetime.datetime.now()
    
    # Format the date and time in a way that's easy to read
    formatted_date = now.strftime("%A, %B %d, %Y")
    formatted_time = now.strftime("%H:%M:%S")
    
    print(f"GOTHAM CITY: {formatted_date}")
    print(f"CURRENT TIME: {formatted_time}")
    
    # Add some crime statistics based on the time (just for fun)
    hour = now.hour
    if 0 <= hour < 6:
        print("CRIME ACTIVITY: High (Night Patrol Recommended)")
    elif 6 <= hour < 12:
        print("CRIME ACTIVITY: Low (Ideal for Bruce Wayne appearances)")
    elif 12 <= hour < 18:
        print("CRIME ACTIVITY: Moderate (Monitor Situation)")
    else:
        print("CRIME ACTIVITY: Increasing (Prepare for Patrol)")
    print()

# List installed Python packages ("gadgets")
def list_gadgets():
    print("AVAILABLE GADGETS (Installed Packages):")
    print("---------------------------------------")
    
    # Get all installed packages
    installed_packages = sorted([f"{d.project_name} {d.version}" 
                               for d in pkg_resources.working_set], 
                              key=lambda x: x.lower())
    
    # Print them in a nice format
    for pkg in installed_packages:
        print(f"- {pkg}")
    print()

# Check for essential packages (Knightfall Protocol challenge)
def check_essential_gadgets():
    essential_gadgets = ["fastapi", "uvicorn", "pydantic", "starlette"]
    installed_pkgs = [d.project_name.lower() for d in pkg_resources.working_set]
    
    missing_gadgets = [pkg for pkg in essential_gadgets 
                      if pkg not in installed_pkgs]
    
    if missing_gadgets:
        print("ALERT: Essential gadgets missing from your utility belt!")
        print("--------------------------------------------------")
        for pkg in missing_gadgets:
            print(f"MISSING: {pkg}")
            print(f"To install: pip install {pkg}")
        print()
    else:
        print("All essential gadgets are installed and ready for use.\n")

def main():
    # Run security check first (Knightfall Protocol challenge)
    security_check()
    
    # Display welcome message with ASCII art
    display_welcome()
    
    # Show current date and time
    show_datetime()
    
    # List installed Python packages ("gadgets")
    list_gadgets()
    
    # Check for essential packages (Knightfall Protocol challenge)
    check_essential_gadgets()
    
    # Batman's signature sign-off
    print("BATMAN OUT.")

if __name__ == "__main__":
    main()
