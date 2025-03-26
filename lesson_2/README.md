# Lesson 2: Gadget Development (Variables, Data Types, Functions)

## Welcome to the Bat-Workshop!

Just as Batman relies on his various gadgets for different situations, Python offers different data types and functions to handle various programming needs. In this lesson, we'll explore how to create and use these tools effectively.

## Learning Objectives
- Master Python's primary data types
- Create and use functions efficiently
- Understand how to import and use modules
- Learn about variable scope and lifetime

## Python Data Types: Batman's Arsenal

### Strings - Your Communication Tools
```python
# Creating strings
villain_name = "Joker"
secret_identity = 'Bruce Wayne'
case_notes = """The suspect was found at the scene,
leaving behind a playing card as a signature."""

# String operations
full_name = "Bruce" + " " + "Wayne"  # Concatenation
bat_signal = "Bat" * 3  # Repetition: "BatBatBat"
shout = "batman".upper()  # Methods: "BATMAN"
whisper = "BATMAN".lower()  # Methods: "batman"

# String formatting
status = f"Batman is currently tracking {villain_name}"
location = "Arkham Asylum"
report = "Villain {} is in {}".format(villain_name, location)
```

### Numbers - Your Measurement Tools
```python
# Integers (whole numbers)
criminals_caught = 10
bat_gadgets = 25

# Floating-point numbers (decimals)
batmobile_speed = 160.5  # mph
reaction_time = 0.23  # seconds

# Numeric operations
total_gadgets = bat_gadgets + 5  # Addition
remaining_fuel = 100 - 25.7  # Subtraction
batarangs_per_villain = criminals_caught / 2  # Division
backup_batteries = 3 ** 2  # Exponentiation (3²)
```

### Booleans - Your Decision Tools
```python
is_night = True
is_batman_revealed = False

# Boolean operations
is_time_to_patrol = is_night and not is_batman_revealed
can_use_batmobile = is_night or is_batman_revealed
need_alfred = not is_night
```

### Lists - Your Collection Tools
```python
# Creating lists
allies = ["Robin", "Nightwing", "Batgirl", "Alfred"]
villain_iq = [180, 165, 140, 157]

# Accessing elements (zero-indexed)
sidekick = allies[0]  # "Robin"
last_villain_iq = villain_iq[-1]  # 157

# Modifying lists
allies.append("Commissioner Gordon")  # Add to end
allies.insert(1, "Catwoman")  # Insert at index 1
allies.remove("Catwoman")  # Remove by value
kicked_out = allies.pop(1)  # Remove by index and return

# Slicing lists
first_two_allies = allies[0:2]  # ["Robin", "Nightwing"]
first_three = allies[:3]  # ["Robin", "Nightwing", "Batgirl"]
last_two = allies[-2:]  # ["Batgirl", "Alfred"]
```

### Dictionaries - Your Data Files
```python
# Creating dictionaries
batmobile = {
    "color": "Black",
    "top_speed": 250,
    "features": ["Rocket Booster", "Stealth Mode", "Machine Guns"],
    "fuel": "Custom Fuel Cell"
}

# Accessing values
color = batmobile["color"]  # "Black"
speed = batmobile.get("top_speed")  # 250

# Modifying dictionaries
batmobile["armor"] = "Titanium Composite"  # Add new key-value pair
batmobile["top_speed"] = 265  # Update existing value
del batmobile["fuel"]  # Remove key-value pair
```

### Tuples - Your Constants
```python
# Creating tuples (immutable lists)
bat_cave_coordinates = (40.8554, -74.2095)
batman_trilogy = ("Batman Begins", "The Dark Knight", "The Dark Knight Rises")

# Accessing tuple elements
latitude = bat_cave_coordinates[0]  # 40.8554
first_movie = batman_trilogy[0]  # "Batman Begins"
```

### Sets - Your Unique Collections
```python
# Creating sets (unordered collections with no duplicates)
known_villains = {"Joker", "Penguin", "Riddler", "Two-Face", "Joker"}
gotham_villains = {"Joker", "Penguin", "Carmine Falcone", "Poison Ivy"}

# Set operations
all_villains = known_villains.union(gotham_villains)  # All unique villains
common_villains = known_villains.intersection(gotham_villains)  # Villains in both sets
unique_to_gotham = gotham_villains - known_villains  # Villains only in gotham_villains
```

## Functions: Batman's Utility Belt

### Basic Functions
```python
# Defining a function
def activate_bat_signal():
    print("The Bat-Signal is activated!")
    print("Batman is on his way.")

# Calling a function
activate_bat_signal()

# Function with parameters
def analyze_criminal(name, danger_level):
    if danger_level > 8:
        return f"{name} is extremely dangerous."
    else:
        return f"{name} is a moderate threat."

# Calling functions with arguments
joker_analysis = analyze_criminal("Joker", 9)
penguin_analysis = analyze_criminal("Penguin", 7)
```

### Function Parameters and Return Values
```python
# Default parameter values
def deploy_vehicle(vehicle_name="Batmobile"):
    return f"Deploying the {vehicle_name}!"

# Optional parameters
batmobile_status = deploy_vehicle()  # Uses default
batwing_status = deploy_vehicle("Batwing")  # Overrides default

# Multiple return values using tuples
def calculate_pursuit_metrics(criminal_speed):
    interception_time = criminal_speed / 10
    fuel_needed = criminal_speed * 0.5
    return interception_time, fuel_needed

# Unpacking return values
time, fuel = calculate_pursuit_metrics(100)
```

### Lambda Functions (Anonymous Functions)
```python
# Quick one-line functions
threat_level = lambda villain, history: villain + history / 10

# Useful with built-in functions like sorted(), map(), filter()
villains = [("Joker", 50), ("Penguin", 30), ("Riddler", 40)]
sorted_by_threat = sorted(villains, key=lambda x: x[1], reverse=True)
```

## Modules: Batman's Support Team

```python
# Importing standard libraries
import random
import datetime
import math

# Importing specific components
from random import choice, randint
from datetime import datetime, timedelta

# Using alias for cleaner code
import numpy as np
import pandas as pd

# Creating and using your own modules
import batman_utilities  # Would import batman_utilities.py
from batman_utilities import track_criminal, analyze_evidence
```

## Project: Batcomputer Criminal Database

Your mission is to create a simple criminal database system for Batman to track Gotham's most wanted. The system should:

1. Store information about multiple criminals using appropriate data structures
2. Provide functions to add criminals, search for criminals, and assess threat levels
3. Allow sorting criminals by different criteria (name, threat level, etc.)
4. Include a simple command-line interface for Batman to interact with the system

Create a file named `criminal_database.py` using the starter code provided.

## The Knightfall Protocol (Push Harder Challenge)

Enhance your criminal database to:
1. Save the database to a file and load it when the program starts
2. Add relationships between criminals (e.g., Joker and Harley Quinn are associates)
3. Implement a simple algorithm to suggest which criminals might be working together based on recent crimes
4. Add a visualization component that displays a "threat map" of Gotham City

## Resources

- Check out `starter_code.py` to get started
- If you need guidance, look at the `helper_guide.md` file for "Bruce Wayne's Journal"
- After you've tried solving it yourself, you can check `solution.py` for one possible implementation

Remember: "It's not just what I do that defines me, but what I use to do it."
