# Lesson 3: Bat-Family Coordination (Control Structures and Error Handling)

## Working as a Team

Just as Batman coordinates with Robin, Nightwing, Batgirl, and others in the field, your code needs to make decisions, handle unexpected situations, and validate inputs. This lesson covers Python's control structures and error handling mechanisms.

## Learning Objectives
- Master control flow structures: if/else statements, loops, and conditionals
- Implement error handling with try/except blocks
- Validate and sanitize user input
- Develop defensive programming techniques

## Control Flow: Batman's Decision Making

### Conditional Statements (if/elif/else)
```python
# Basic if statement
if is_night:
    deploy_batman()

# if/else statement
if criminal_count > 5:
    request_backup()
else:
    proceed_solo()

# if/elif/else for multiple conditions
threat_level = assess_threat(villain)
if threat_level >= 8:
    alert_gordon()
    use_special_equipment()
elif threat_level >= 5:
    use_standard_tactics()
else:
    use_stealth_approach()
```

### Nested Conditions
```python
if is_night:
    if is_raining:
        use_waterproof_cape()
    else:
        use_regular_cape()
else:
    wear_bruce_wayne_suit()
```

### Conditional Expressions (Ternary Operator)
```python
# Instead of:
if is_night:
    vehicle = "Batmobile"
else:
    vehicle = "Lamborghini"

# You can write:
vehicle = "Batmobile" if is_night else "Lamborghini"
```

## Loops: Patrolling Gotham

### For Loops
```python
# Iterating through a list
for ally in bat_family:
    assign_patrol_area(ally)

# Using range
for i in range(5):  # 0 to 4
    launch_batarang()

# Enumerate for index and value
for index, villain in enumerate(rogues_gallery):
    print(f"Villain #{index+1}: {villain}")

# Loop with dictionary
for name, abilities in villains.items():
    print(f"{name} has abilities: {abilities}")
```

### While Loops
```python
# Basic while loop
bat_signal_active = True
while bat_signal_active:
    check_crime_reports()
    if no_crimes_reported():
        bat_signal_active = False

# With a counter
patrol_count = 0
while patrol_count < 3:
    patrol_gotham()
    patrol_count += 1
    
# Infinite loop with break
while True:
    crime = check_for_crimes()
    if crime is None:
        break  # Exit the loop
    respond_to_crime(crime)
```

### Loop Control Statements
```python
# break - exit the loop
for area in gotham_areas:
    if joker_detected(area):
        print(f"Joker found in {area}!")
        break  # Stop the search once found

# continue - skip to the next iteration
for villain in criminals:
    if villain.threat_level < 5:
        continue  # Skip low-threat villains
    engage(villain)
    
# pass - placeholder for future code
for ally in missing_allies:
    pass  # Will implement search protocol later
```

## Error Handling: Contingency Plans

### Basic Try/Except
```python
try:
    batcomputer_data = access_database("criminals")
    process_data(batcomputer_data)
except:
    print("Error accessing database")
```

### Handling Specific Exceptions
```python
try:
    file = open("bat_cave_security.log", "r")
    contents = file.read()
    file.close()
except FileNotFoundError:
    print("Security log not found, creating new log file")
    file = open("bat_cave_security.log", "w")
    file.close()
except PermissionError:
    print("Access denied to security logs")
```

### The else and finally Clauses
```python
try:
    criminal_data = get_criminal_data("Joker")
    decode_data(criminal_data)
except ConnectionError:
    print("Cannot connect to Batcomputer network")
except ValueError:
    print("Invalid criminal ID")
else:
    # Executes if no exceptions occurred
    print("Criminal data retrieved successfully")
finally:
    # Always executes, regardless of exceptions
    close_connection()
    print("Database operation completed")
```

### Custom Exceptions
```python
# Define custom exceptions
class BatcaveSecurityException(Exception):
    pass

class IntruderAlertException(BatcaveSecurityException):
    def __init__(self, location, threat_level):
        self.location = location
        self.threat_level = threat_level
        super().__init__(f"Intruder detected at {location}, threat level: {threat_level}")

# Raise custom exceptions
def check_security():
    if detect_intruder():
        location = get_intruder_location()
        threat = assess_threat_level()
        raise IntruderAlertException(location, threat)
```

## Input Validation: Interrogation Techniques

### Basic Input Validation
```python
user_input = input("Enter criminal name: ")

# Check if input is empty
if not user_input:
    print("Error: Name cannot be empty")

# Check input length
if len(user_input) < 3:
    print("Error: Name too short")

# Check for numeric input when required
try:
    threat_level = int(input("Enter threat level (1-10): "))
    if not 1 <= threat_level <= 10:
        print("Error: Threat level must be between 1 and 10")
except ValueError:
    print("Error: Please enter a valid number")
```

### Input Sanitization
```python
# Convert to consistent case
criminal_name = user_input.strip().lower()

# Remove special characters
import re
clean_name = re.sub(r'[^a-zA-Z0-9]', '', criminal_name)

# Validate email format
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
if not re.match(email_pattern, email):
    print("Invalid email format")
```

## Project: Gotham Night Patrol Simulator

Your mission is to create a program that simulates Batman and allies patrolling different areas of Gotham. The system should:

1. Use control structures to dispatch heroes to different areas based on crime levels
2. Randomly generate "crime events" in different districts
3. Implement error handling for various scenarios
4. Validate user input for patrol configuration

Create a file named `night_patrol.py` using the starter code provided.

## The Knightfall Protocol (Push Harder Challenge)

Enhance your patrol simulator to:
1. Implement a priority system that handles multiple crisis events happening simultaneously
2. Make optimal dispatching decisions based on hero specialties and threat types
3. Create a custom exception hierarchy for different types of patrol emergencies
4. Implement a patrol log that records all activities, successes, and failures

## Resources

- Check out `starter_code.py` to get started
- If you need guidance, look at the `helper_guide.md` file for "Bruce Wayne's Journal"
- After you've tried solving it yourself, you can check `solution.py` for one possible implementation

Remember, in Batman's words: "It's not who I am underneath, but what I do that defines me."
