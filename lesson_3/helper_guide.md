# Bruce Wayne's Journal: Gotham Night Patrol Simulator

## Thought Process

When designing a patrol simulator for Gotham City, we need to consider how Batman and the Bat-Family coordinate their efforts effectively. This requires careful use of control structures and error handling to ensure a robust system.

### 1. Generating Random Crime Events

**Thought process:**
- Need to simulate unpredictable crime patterns across Gotham
- Crime severity should vary to test our dispatch prioritization
- Events should occur in different locations to spread our resources
- Should handle the scenario where multiple simultaneous crimes occur

**Pseudo-code:**
```
Function generate_crime_events(num_events=None):
    If num_events is not specified:
        Randomly determine how many events to generate (1-3)
    
    Initialize empty list for events
    
    For each event:
        Randomly select a crime type
        Randomly select a location
        Determine severity (1-10) with super-villain activity being higher
        Create event dictionary and append to list
    
    Return the list of crime events
```

### 2. Validating Patrol Configuration

**Thought process:**
- We must ensure the input makes logical sense
- Need to validate that we have enough heroes for the areas we want to patrol
- Input should be within reasonable bounds
- Any validation failure should raise appropriate exceptions

**Pseudo-code:**
```
Function validate_patrol_config(num_heroes, num_areas):
    If num_heroes is not an integer or less than 1:
        Raise ValueError with appropriate message
    
    If num_heroes is greater than available heroes:
        Raise ValueError with appropriate message
    
    If num_areas is not an integer or less than 1:
        Raise ValueError with appropriate message
    
    If num_areas is greater than available areas:
        Raise ValueError with appropriate message
    
    If num_heroes < num_areas:
        Raise ValueError explaining we need at least one hero per area
    
    Return True if all validations pass
```

### 3. Dispatching Heroes to Crimes

**Thought process:**
- Different heroes have different specialties and effectiveness
- Success should depend on hero's capabilities vs. crime severity
- Need to account for randomness (even Batman doesn't succeed 100% of the time)
- The system should report the outcome clearly

**Pseudo-code:**
```
Function dispatch_hero(hero, area, crime):
    Calculate base success chance from hero's effectiveness
    
    Apply modifiers:
        If hero's specialty matches crime type, increase chance
        If crime severity is high, decrease chance
    
    Generate random number to determine success or failure
    
    If successful:
        Return success message with details
    Else:
        Return failure message with details
```

### 4. Running the Patrol Simulation

**Thought process:**
- Need to orchestrate the whole simulation
- Should handle unexpected errors gracefully
- Need to present a clear sequence of events to the user
- Should maintain the state of heroes and crime throughout the simulation

**Pseudo-code:**
```
Function run_patrol(num_heroes, num_areas):
    Try:
        Validate patrol configuration
        
        Select random heroes based on num_heroes
        Select random areas based on num_areas
        
        Generate crime events
        
        For each area under patrol:
            Check if a crime is happening there
            If yes, dispatch an available hero
            Record the outcome
        
        Handle any unattended crimes (for Knightfall Protocol)
        
        Report overall success/failure
    
    Except specific exceptions:
        Handle each exception appropriately
        
    Except general Exception:
        Log the unexpected error
        Return failure
        
    Return success
```

## Implementation Hints

### Crime Generation:
```python
def generate_crime_events(num_events=None):
    if num_events is None:
        num_events = random.randint(1, 3)
    
    events = []
    used_areas = set()  # To ensure no duplicate locations
    
    for _ in range(num_events):
        crime_type = random.choice(CRIME_TYPES)
        
        # Find an area not already used
        available_areas = [area for area in GOTHAM_AREAS if area not in used_areas]
        if not available_areas:  # If all areas have crimes (unlikely)
            break
        
        location = random.choice(available_areas)
        used_areas.add(location)
        
        # Super-villain activity is more severe
        if crime_type == "Super-villain Activity":
            severity = random.randint(7, 10)
        else:
            severity = random.randint(3, 8)
        
        events.append({
            "type": crime_type,
            "location": location,
            "severity": severity
        })
    
    return events
```

### Validation with Exception Handling:
```python
def validate_patrol_config(num_heroes, num_areas):
    try:
        num_heroes = int(num_heroes)
        num_areas = int(num_areas)
    except ValueError:
        raise ValueError("The number of heroes and areas must be integers.")
    
    if num_heroes < 1:
        raise ValueError("At least one hero must be deployed.")
    
    if num_heroes > len(BAT_FAMILY):
        raise ValueError(f"There are only {len(BAT_FAMILY)} heroes available.")
    
    if num_areas < 1:
        raise ValueError("At least one area must be patrolled.")
    
    if num_areas > len(GOTHAM_AREAS):
        raise ValueError(f"There are only {len(GOTHAM_AREAS)} areas to patrol.")
    
    if num_heroes < num_areas:
        raise ValueError("Each area needs at least one hero. Deploy more heroes or patrol fewer areas.")
    
    return True
```

### For the Knightfall Protocol (Push Harder Challenge)

#### Custom Exception Hierarchy:
```python
class PatrolException(Exception):
    """Base exception for patrol-related errors."""
    pass

class ResourceException(PatrolException):
    """Exception for resource allocation issues."""
    pass

class CrisisException(PatrolException):
    """Exception for critical situations."""
    def __init__(self, location, severity, message=None):
        self.location = location
        self.severity = severity
        if message is None:
            message = f"Crisis at {location} with severity {severity}"
        super().__init__(message)
```

#### Priority System:
```python
def prioritize_crimes(crimes):
    """Sort crimes by severity and type."""
    priority_order = {
        "Super-villain Activity": 1,
        "Kidnapping": 2,
        "Assault": 3,
        "Robbery": 4,
        "Illegal Weapons": 5,
        "Drug Deal": 6
    }
    
    # Sort by severity first, then by crime type priority
    return sorted(crimes, key=lambda c: (-c["severity"], priority_order.get(c["type"], 999)))
```

#### Match Heroes to Crimes:
```python
def match_hero_to_crime(heroes, crime):
    """Find the best hero for a specific crime."""
    # Define specialty effectiveness for different crime types
    specialty_matching = {
        "Robbery": ["Combat", "Stealth"],
        "Assault": ["Combat", "Acrobatics"],
        "Kidnapping": ["Stealth", "Combat"],
        "Drug Deal": ["Stealth", "Firearms"],
        "Illegal Weapons": ["Firearms", "Combat"],
        "Super-villain Activity": ["Combat", "Acrobatics", "Firearms"]
    }
    
    best_match = None
    best_score = -1
    
    for hero in heroes:
        # Base score is hero effectiveness
        score = hero["effectiveness"]
        
        # Bonus for specialty match
        if hero["specialty"] in specialty_matching.get(crime["type"], []):
            score += 3
        
        # Batman gets a bonus for everything
        if hero["name"] == "Batman":
            score += 2
        
        if score > best_score:
            best_score = score
            best_match = hero
    
    return best_match
```

Remember: "In our line of work, you prepare for every eventuality."
