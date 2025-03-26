#!/usr/bin/env python3
"""
Gotham Night Patrol Simulator - Complete Solution
----------------------------
A fully implemented patrol simulator with Knightfall Protocol enhancements.
"""
import random
import time
import os
from datetime import datetime

# Custom exceptions for the Knightfall Protocol
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

# Define Gotham City areas
GOTHAM_AREAS = [
    "Amusement Mile", 
    "Diamond District",
    "East End", 
    "Financial District", 
    "Gotham Heights",
    "Robinson Park", 
    "Chinatown", 
    "Arkham Asylum"
]

# Define the Bat-Family (patrol team)
BAT_FAMILY = [
    {"name": "Batman", "specialty": "Combat", "effectiveness": 10},
    {"name": "Robin", "specialty": "Acrobatics", "effectiveness": 7},
    {"name": "Batgirl", "specialty": "Hacking", "effectiveness": 8},
    {"name": "Nightwing", "specialty": "Stealth", "effectiveness": 9},
    {"name": "Red Hood", "specialty": "Firearms", "effectiveness": 8},
]

# Define crime types and their specialty matches
CRIME_TYPES = [
    "Robbery", 
    "Assault", 
    "Kidnapping", 
    "Drug Deal", 
    "Illegal Weapons", 
    "Super-villain Activity"
]

# Specialty effectiveness for different crime types
SPECIALTY_MATCHING = {
    "Robbery": ["Combat", "Stealth"],
    "Assault": ["Combat", "Acrobatics"],
    "Kidnapping": ["Stealth", "Combat"],
    "Drug Deal": ["Stealth", "Firearms"],
    "Illegal Weapons": ["Firearms", "Combat"],
    "Super-villain Activity": ["Combat", "Acrobatics", "Firearms"]
}

# Crime priority order (lower number = higher priority)
CRIME_PRIORITY = {
    "Super-villain Activity": 1,
    "Kidnapping": 2,
    "Assault": 3,
    "Robbery": 4,
    "Illegal Weapons": 5,
    "Drug Deal": 6
}

# Patrol log setup (Knightfall Protocol)
def setup_patrol_log():
    """Set up the patrol log file."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"patrol_log_{timestamp}.txt")
    
    return log_file

def log_patrol_event(log_file, message):
    """Log an event to the patrol log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    with open(log_file, "a") as f:
        f.write(log_entry)
    
    # Also print to console
    print(message)

def generate_crime_events(num_events=None):
    """Generate random crime events in different areas of Gotham."""
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
            "severity": severity,
            "status": "Active"  # For tracking whether it's been handled
        })
    
    return events

def validate_patrol_config(num_heroes, num_areas):
    """Validate user input for patrol configuration."""
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
    
    return True

def dispatch_hero(hero, crime, log_file=None):
    """Dispatch a hero to handle a crime in a specific area."""
    # Calculate base success chance from hero effectiveness
    base_chance = hero["effectiveness"] * 10  # Convert to percentage (0-100)
    
    # Apply modifiers
    # Specialty bonus
    specialty_bonus = 0
    if hero["specialty"] in SPECIALTY_MATCHING.get(crime["type"], []):
        specialty_bonus = 20
        if log_file:
            log_patrol_event(log_file, f"{hero['name']}'s {hero['specialty']} specialty is effective against {crime['type']}!")
    
    # Severity penalty
    severity_penalty = crime["severity"] * 5
    
    # Batman gets an additional bonus because he's Batman
    batman_bonus = 15 if hero["name"] == "Batman" else 0
    
    # Calculate final success chance
    success_chance = min(95, base_chance + specialty_bonus - severity_penalty + batman_bonus)
    success_chance = max(5, success_chance)  # Always at least 5% chance
    
    # Roll for success
    roll = random.randint(1, 100)
    success = roll <= success_chance
    
    # Prepare result
    area = crime["location"]
    
    if success:
        result = {
            "success": True,
            "message": f"{hero['name']} successfully stopped the {crime['type']} in {area}.",
            "details": f"Success chance: {success_chance}%, Roll: {roll}"
        }
    else:
        result = {
            "success": False,
            "message": f"{hero['name']} failed to stop the {crime['type']} in {area}.",
            "details": f"Success chance: {success_chance}%, Roll: {roll}"
        }
    
    # Log the result
    if log_file:
        log_patrol_event(log_file, result["message"])
        log_patrol_event(log_file, f"Details: {result['details']}")
    
    return result

def prioritize_crimes(crimes):
    """Sort crimes by severity and type (Knightfall Protocol)."""
    # Sort by severity first (descending), then by crime type priority
    return sorted(crimes, key=lambda c: (-c["severity"], CRIME_PRIORITY.get(c["type"], 999)))

def match_hero_to_crime(available_heroes, crime, log_file=None):
    """Find the best hero for a specific crime (Knightfall Protocol)."""
    if not available_heroes:
        if log_file:
            log_patrol_event(log_file, "No heroes available to handle crime!")
        return None
    
    best_hero = None
    best_score = -1
    
    for hero in available_heroes:
        # Base score is hero effectiveness
        score = hero["effectiveness"]
        
        # Bonus for specialty match
        if hero["specialty"] in SPECIALTY_MATCHING.get(crime["type"], []):
            score += 3
        
        # Batman gets a bonus for everything
        if hero["name"] == "Batman":
            score += 2
        
        if score > best_score:
            best_score = score
            best_hero = hero
    
    if log_file and best_hero:
        log_patrol_event(log_file, f"Selected {best_hero['name']} (score: {best_score}) for {crime['type']} in {crime['location']}")
    
    return best_hero

def run_patrol(num_heroes, num_areas):
    """Run the main patrol simulation."""
    # Set up patrol log
    log_file = setup_patrol_log()
    log_patrol_event(log_file, "===== GOTHAM NIGHT PATROL BEGINNING =====")
    log_patrol_event(log_file, f"Deploying {num_heroes} heroes to patrol {num_areas} areas")
    
    try:
        # Validate patrol configuration
        validate_patrol_config(num_heroes, num_areas)
        
        # Select heroes for patrol
        selected_heroes = random.sample(BAT_FAMILY, num_heroes)
        available_heroes = selected_heroes.copy()  # Track which heroes are available
        
        # Select areas to patrol
        patrol_areas = random.sample(GOTHAM_AREAS, num_areas)
        
        log_patrol_event(log_file, "\n=== PATROL TEAM ===")
        for hero in selected_heroes:
            log_patrol_event(log_file, f"{hero['name']} - Specialty: {hero['specialty']}, Effectiveness: {hero['effectiveness']}/10")
        
        log_patrol_event(log_file, "\n=== PATROL AREAS ===")
        for area in patrol_areas:
            log_patrol_event(log_file, f"Patrolling: {area}")
        
        # Generate crime events
        crime_events = generate_crime_events()
        
        log_patrol_event(log_file, f"\n=== REPORTED CRIMES ({len(crime_events)}) ===")
        for i, crime in enumerate(crime_events, 1):
            log_patrol_event(log_file, f"Crime #{i}: {crime['type']} in {crime['location']} (Severity: {crime['severity']}/10)")
        
        # Check if any crimes are in areas we're not patrolling
        unpatrolled_crimes = [c for c in crime_events if c["location"] not in patrol_areas]
        if unpatrolled_crimes:
            log_patrol_event(log_file, f"\nWARNING: {len(unpatrolled_crimes)} crimes detected outside patrol areas!")
            
            # For Knightfall Protocol: Decide whether to reallocate resources
            if len(unpatrolled_crimes) > 0 and random.random() < 0.7:  # 70% chance to reallocate
                highest_priority = prioritize_crimes(unpatrolled_crimes)[0]
                log_patrol_event(log_file, f"High-priority situation detected: {highest_priority['type']} in {highest_priority['location']}!")
                log_patrol_event(log_file, "Reallocating resources to respond...")
                
                # Add the high-priority area to our patrol
                patrol_areas.append(highest_priority["location"])
                
                # If we don't have enough heroes, raise an exception
                if len(available_heroes) == 0:
                    raise ResourceException("No available heroes to respond to the crisis!")
        
        # Process crimes in order of priority (Knightfall Protocol)
        prioritized_crimes = prioritize_crimes(crime_events)
        
        log_patrol_event(log_file, "\n=== BEGINNING PATROL OPERATIONS ===")
        
        # Track results
        successes = 0
        failures = 0
        unhandled = 0
        
        # Handle each crime in priority order
        for crime in prioritized_crimes:
            time.sleep(0.5)  # Simulate passage of time
            
            # Check if the crime is in a patrolled area
            if crime["location"] in patrol_areas:
                # Find the best hero for this crime
                best_hero = match_hero_to_crime(available_heroes, crime, log_file)
                
                if best_hero:
                    # Remove hero from available list
                    available_heroes = [h for h in available_heroes if h["name"] != best_hero["name"]]
                    
                    # Dispatch the hero
                    result = dispatch_hero(best_hero, crime, log_file)
                    
                    # Update statistics
                    if result["success"]:
                        successes += 1
                        crime["status"] = "Resolved"
                    else:
                        failures += 1
                        crime["status"] = "Failed"
                    
                    # Hero becomes available again after some time
                    time.sleep(1)  # Simulate hero returning
                    available_heroes.append(best_hero)
                    log_patrol_event(log_file, f"{best_hero['name']} is available for patrol again.")
                else:
                    log_patrol_event(log_file, f"No heroes available to handle {crime['type']} in {crime['location']}!")
                    unhandled += 1
                    crime["status"] = "Unhandled"
            else:
                log_patrol_event(log_file, f"{crime['type']} in {crime['location']} is outside patrol areas.")
                unhandled += 1
                crime["status"] = "Outside Patrol"
        
        # Patrol summary
        log_patrol_event(log_file, "\n=== PATROL SUMMARY ===")
        log_patrol_event(log_file, f"Crimes successfully stopped: {successes}")
        log_patrol_event(log_file, f"Failed attempts: {failures}")
        log_patrol_event(log_file, f"Unhandled crimes: {unhandled}")
        
        # Final status report
        log_patrol_event(log_file, "\n=== FINAL CRIME STATUS ===")
        for crime in crime_events:
            log_patrol_event(log_file, f"{crime['type']} in {crime['location']} - Status: {crime['status']}")
        
        # Overall success?
        patrol_success = successes > failures and unhandled <= 1
        status = "SUCCESSFUL" if patrol_success else "PROBLEMATIC"
        log_patrol_event(log_file, f"\nPatrol deemed {status}.")
        log_patrol_event(log_file, "===== GOTHAM NIGHT PATROL COMPLETE =====")
        
        return patrol_success
    
    except ResourceException as e:
        log_patrol_event(log_file, f"\nRESOURCE ERROR: {e}")
        log_patrol_event(log_file, "Requesting additional Bat-Family members for backup!")
        return False
    
    except CrisisException as e:
        log_patrol_event(log_file, f"\nCRISIS ALERT: {e}")
        log_patrol_event(log_file, f"Emergency response needed at {e.location}!")
        return False
    
    except ValueError as e:
        log_patrol_event(log_file, f"\nCONFIGURATION ERROR: {e}")
        return False
    
    except Exception as e:
        log_patrol_event(log_file, f"\nUNEXPECTED ERROR: {e}")
        return False

def main():
    """Main function to run the Gotham Night Patrol Simulator."""
    print("\n===== GOTHAM NIGHT PATROL SIMULATOR =====")
    print("Configure the night's patrol parameters:")
    
    try:
        # Try to get configuration from user
        while True:
            try:
                num_heroes = int(input("Number of heroes to deploy (1-5): "))
                num_areas = int(input("Number of areas to patrol (1-8): "))
                
                # Validate input basic ranges
                if 1 <= num_heroes <= 5 and 1 <= num_areas <= 8:
                    break
                else:
                    print("Please enter values within the specified ranges.")
            except ValueError:
                print("Please enter valid numbers.")
        
        # Run the patrol simulation
        print("\nInitiating patrol sequence...")
        success = run_patrol(num_heroes, num_areas)
        
        if success:
            print("\nPatrol completed successfully. Returning to the Batcave.")
        else:
            print("\nPatrol encountered issues. Review the patrol log for details.")
            
    except KeyboardInterrupt:
        print("\n\nPatrol simulation aborted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    
    print("\nPatrol logs saved. BATMAN OUT.")

if __name__ == "__main__":
    main()
