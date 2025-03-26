# Lesson 1: The Dark Knight Begins (Python Basics)

## Welcome to the Batcave!

Just as Bruce Wayne needed to establish his Batcave before becoming Batman, we need to set up our development environment before we can start coding with FastAPI.

## Learning Objectives
- Set up a Python development environment
- Understand Python syntax and basic commands
- Run your first Python script
- Get a glimpse of FastAPI's potential

## The Batcave Setup (Environment Setup)

### 1. Installing Python
If you don't have Python installed, download and install it from [python.org](https://python.org). Batman recommends Python 3.8 or later.

### 2. Setting Up a Virtual Environment
Just as Batman keeps his equipment organized, we'll keep our Python packages isolated using a virtual environment:

```bash
# Create a virtual environment
python -m venv batcave-env

# Activate it (on Windows)
batcave-env\Scripts\activate

# Activate it (on macOS/Linux)
source batcave-env/bin/activate
```

### 3. Installing Essential Gadgets (Packages)
```bash
# Install FastAPI and Uvicorn (our ASGI server)
pip install fastapi uvicorn
```

## Basic Python Concepts

### Variables and Data Types
```python
# Strings
bat_signal = "Active"
vigilante_name = "Batman"

# Numbers
criminals_caught = 10
years_active = 8.5

# Booleans
is_bruce_wayne = True
is_batman_identity_public = False

# Lists (collections of items)
bat_gadgets = ["Batarang", "Grappling Hook", "Smoke Pellets"]

# Dictionaries (key-value pairs)
batmobile = {
    "color": "Black",
    "top_speed": 250,
    "weapons": ["Machine Guns", "Missile Launchers"],
    "autopilot": True
}
```

### Basic Operations
```python
# String operations
full_identity = vigilante_name + " is " + "Bruce Wayne"
bat_signal_status = f"The Bat-Signal is {bat_signal}"

# Numerical operations
total_crimefighting_years = years_active + 2.5

# List operations
bat_gadgets.append("Batcomputer Remote")
first_gadget = bat_gadgets[0]

# Dictionary operations
batmobile["location"] = "Batcave"
batmobile_speed = batmobile["top_speed"]
```

### Control Flow
```python
# If statements
if bat_signal == "Active":
    print("Batman is on his way!")
elif bat_signal == "Inactive" and is_bruce_wayne:
    print("Bruce Wayne is attending to business matters.")
else:
    print("It's a quiet night in Gotham.")

# Loops
for gadget in bat_gadgets:
    print(f"Batman equipped: {gadget}")

villain_attempts = 0
while villain_attempts < 3:
    print(f"The Joker's escape attempt #{villain_attempts + 1} failed!")
    villain_attempts += 1
```

### Functions
```python
def activate_bat_signal():
    return "Batman has been summoned to fight crime!"

def analyze_criminal(name, danger_level):
    if danger_level > 8:
        return f"{name} is extremely dangerous. Proceed with caution."
    else:
        return f"{name} is a moderate threat. Standard protocol advised."

# Function calls
signal_result = activate_bat_signal()
joker_analysis = analyze_criminal("Joker", 9)
```

## Project: Batcave Initialization System

Your first mission as Bruce Wayne's new tech assistant is to create a simple Python script that:

1. Prints a welcome message to the "Batcave Terminal"
2. Shows the current date/time (Batman needs to know when crime typically happens)
3. Lists your available "gadgets" (installed Python packages)

Create a file named `batcave_init.py` using the starter code provided.

## The Knightfall Protocol (Push Harder Challenge)

Modify your script to:
1. Check if certain "essential gadgets" (packages like fastapi, uvicorn) are installed
2. If not, suggest installation commands
3. Add a basic security check that asks for a password before allowing access

## How to Run Your Script

```bash
python batcave_init.py
```

## Resources

- Check out `starter_code.py` to get started
- If you need guidance, look at the `helper_guide.md` file for "Bruce Wayne's Journal"
- After you've tried solving it yourself, you can check `solution.py` for one possible implementation

Remember, in the words of Alfred Pennyworth: "Why do we fall, sir? So that we can learn to pick ourselves up."
