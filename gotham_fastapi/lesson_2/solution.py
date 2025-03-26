#!/usr/bin/env python3
"""
Batcomputer Criminal Database - Complete Solution
----------------------------
A fully implemented criminal database system for Batman
including the Knightfall Protocol enhancements.
"""
import json
import os
import datetime
import random

# Initialize the criminals database
# We'll add some sample data to start with
criminals = [
    {
        "id": 1,
        "name": "Joker",
        "alias": "Unknown",
        "physical": {
            "height": 6.1,
            "weight": 180,
            "hair": "Green",
            "eyes": "Green"
        },
        "abilities": ["Chemical expertise", "Psychological manipulation", "Hand-to-hand combat"],
        "threat_level": 9,
        "status": "At large",
        "last_seen": "Amusement Mile",
        "associates": ["Harley Quinn"],
        "recent_crimes": ["Bank robbery", "Chemical attack", "Mass breakout at Arkham"]
    },
    {
        "id": 2,
        "name": "Oswald Cobblepot",
        "alias": "Penguin",
        "physical": {
            "height": 5.2,
            "weight": 175,
            "hair": "Black",
            "eyes": "Blue"
        },
        "abilities": ["Criminal mastermind", "Weapons trafficking", "Business operations"],
        "threat_level": 7,
        "status": "Under surveillance",
        "last_seen": "Iceberg Lounge",
        "associates": ["Riddler", "Black Mask"],
        "recent_crimes": ["Weapons smuggling", "Money laundering", "Extortion"]
    },
    {
        "id": 3,
        "name": "Edward Nygma",
        "alias": "Riddler",
        "physical": {
            "height": 6.0,
            "weight": 170,
            "hair": "Brown",
            "eyes": "Blue"
        },
        "abilities": ["Genius-level intellect", "Engineering", "Puzzle design"],
        "threat_level": 8,
        "status": "Incarcerated",
        "last_seen": "Arkham Asylum",
        "associates": ["Penguin", "Two-Face"],
        "recent_crimes": ["Cyber attack", "Hostage situation", "Death trap setup"]
    },
    {
        "id": 4,
        "name": "Harleen Quinzel",
        "alias": "Harley Quinn",
        "physical": {
            "height": 5.7,
            "weight": 140,
            "hair": "Blonde (often dyed)",
            "eyes": "Blue"
        },
        "abilities": ["Gymnastics", "Immunity to toxins", "Psychology expertise"],
        "threat_level": 7,
        "status": "At large",
        "last_seen": "Amusement Mile",
        "associates": ["Joker", "Poison Ivy"],
        "recent_crimes": ["Armed robbery", "Assault", "Aiding and abetting"]
    },
    {
        "id": 5,
        "name": "Pamela Isley",
        "alias": "Poison Ivy",
        "physical": {
            "height": 5.8,
            "weight": 145,
            "hair": "Red",
            "eyes": "Green"
        },
        "abilities": ["Toxin immunity", "Botanical control", "Pheromone manipulation"],
        "threat_level": 8,
        "status": "At large",
        "last_seen": "Robinson Park",
        "associates": ["Harley Quinn"],
        "recent_crimes": ["Eco-terrorism", "Kidnapping", "Assault"]
    }
]

# File operations for persistence (Knightfall Protocol)
def save_database(filename="criminals.json"):
    """Save the criminal database to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(criminals, f, indent=4)
    print(f"\nBatcomputer: Database saved to {filename}")

def load_database(filename="criminals.json"):
    """Load the criminal database from a JSON file."""
    global criminals
    try:
        with open(filename, 'r') as f:
            criminals = json.load(f)
        print(f"\nBatcomputer: Database loaded from {filename}")
    except FileNotFoundError:
        print("\nBatcomputer: No existing database found. Starting with sample data.")


# Core database functions
def add_criminal():
    """Add a new criminal to the database."""
    print("\n===== ADD NEW CRIMINAL =====")
    
    # Get the next available ID
    next_id = max([c["id"] for c in criminals], default=0) + 1
    
    # Get criminal details from user input
    name = input("Name: ")
    alias = input("Alias (if known): ")
    
    # Physical characteristics
    print("\nPhysical characteristics:")
    try:
        height = float(input("Height (ft): "))
        weight = float(input("Weight (lbs): "))
    except ValueError:
        print("Invalid input. Using default values.")
        height = 6.0
        weight = 170
        
    hair = input("Hair color: ")
    eyes = input("Eye color: ")
    
    # Abilities
    abilities = []
    print("\nAbilities (enter 'done' when finished):")
    while True:
        ability = input("Ability: ")
        if ability.lower() == 'done':
            break
        abilities.append(ability)
    
    # Threat assessment
    try:
        threat_level = int(input("\nThreat level (1-10): "))
        if threat_level < 1 or threat_level > 10:
            print("Invalid threat level. Setting to default of 5.")
            threat_level = 5
    except ValueError:
        print("Invalid input. Setting threat level to default of 5.")
        threat_level = 5
    
    # Status and location
    status = input("\nCurrent status: ")
    last_seen = input("Last known location: ")
    
    # Associates (Knightfall Protocol)
    associates = []
    print("\nKnown associates (enter 'done' when finished):")
    while True:
        associate = input("Associate: ")
        if associate.lower() == 'done':
            break
        associates.append(associate)
    
    # Recent crimes (Knightfall Protocol)
    recent_crimes = []
    print("\nRecent crimes (enter 'done' when finished):")
    while True:
        crime = input("Crime: ")
        if crime.lower() == 'done':
            break
        recent_crimes.append(crime)
    
    # Create the criminal record
    criminal = {
        "id": next_id,
        "name": name,
        "alias": alias,
        "physical": {
            "height": height,
            "weight": weight,
            "hair": hair,
            "eyes": eyes
        },
        "abilities": abilities,
        "threat_level": threat_level,
        "status": status,
        "last_seen": last_seen,
        "associates": associates,
        "recent_crimes": recent_crimes
    }
    
    # Add to database
    criminals.append(criminal)
    print(f"\nCriminal {name} added to database.")
    
    # Save database (Knightfall Protocol)
    save_database()

def search_criminal():
    """Search for criminals by name or alias."""
    print("\n===== SEARCH CRIMINAL DATABASE =====")
    search_term = input("Enter search term: ")
    
    results = []
    for criminal in criminals:
        if (search_term.lower() in criminal["name"].lower() or 
            search_term.lower() in criminal["alias"].lower()):
            results.append(criminal)
    
    if results:
        print(f"\nFound {len(results)} matching criminals:")
        for criminal in results:
            display_criminal(criminal)
    else:
        print("\nNo matching criminals found.")

def assess_threat():
    """Assess and calculate the threat level of a criminal."""
    print("\n===== THREAT ASSESSMENT =====")
    name = input("Enter criminal name: ")
    
    # Find the criminal
    found = False
    for criminal in criminals:
        if name.lower() in criminal["name"].lower() or name.lower() in criminal["alias"].lower():
            found = True
            
            # Base threat is their assigned threat_level
            base_threat = criminal["threat_level"]
            
            # Adjust based on abilities
            ability_factor = len(criminal["abilities"]) * 0.5
            
            # Adjust based on status
            status_modifier = 1.5 if criminal["status"].lower() == "at large" else 0.7
            
            # Adjust based on associates (Knightfall Protocol)
            associate_factor = len(criminal["associates"]) * 0.3
            
            # Calculate final threat score
            final_threat = base_threat + ability_factor * status_modifier + associate_factor
            final_threat = min(10, final_threat)  # Cap at 10
            
            # Display the assessment
            print(f"\nThreat Assessment for {criminal['name']} ({criminal['alias']}):")
            print(f"Base Threat Level: {base_threat}")
            print(f"Ability Modifier: +{ability_factor:.1f}")
            print(f"Status Modifier: x{status_modifier:.1f}")
            print(f"Associate Factor: +{associate_factor:.1f}")
            print(f"FINAL THREAT SCORE: {final_threat:.1f}/10")
            
            # Recommendations
            print("\nRecommendations:")
            if final_threat >= 9:
                print("EXTREME CAUTION ADVISED. Full bat-suit and specialized equipment required.")
                print("Alert Gordon and consider team backup.")
            elif final_threat >= 7:
                print("HIGH THREAT LEVEL. Standard precautions and bat-suit advised.")
                print("Consider additional equipment based on abilities.")
            elif final_threat >= 5:
                print("MODERATE THREAT. Standard approach should be sufficient.")
                print("Remain vigilant for unexpected abilities.")
            else:
                print("LOW THREAT. Minimal equipment needed.")
                print("Standard apprehension protocols should suffice.")
                
            break
    
    if not found:
        print(f"Criminal '{name}' not found in database.")

def sort_criminals():
    """Sort and display criminals by different criteria."""
    print("\n===== SORT CRIMINALS =====")
    print("Sort by:")
    print("1. Name")
    print("2. Threat Level")
    print("3. Status")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == '1':
        sorted_criminals = sorted(criminals, key=lambda x: x["name"])
        criterion = "Name"
    elif choice == '2':
        sorted_criminals = sorted(criminals, key=lambda x: x["threat_level"], reverse=True)
        criterion = "Threat Level (Highest to Lowest)"
    elif choice == '3':
        sorted_criminals = sorted(criminals, key=lambda x: x["status"])
        criterion = "Status"
    else:
        print("Invalid choice. Sorting by name by default.")
        sorted_criminals = sorted(criminals, key=lambda x: x["name"])
        criterion = "Name"
    
    print(f"\nCriminals sorted by {criterion}:")
    for criminal in sorted_criminals:
        print(f"{criminal['name']} ({criminal['alias']}) - "
              f"Threat: {criminal['threat_level']}, Status: {criminal['status']}")

def display_criminals():
    """Display all criminals in the database."""
    print(f"\n===== ALL CRIMINALS ({len(criminals)}) =====")
    for criminal in criminals:
        display_criminal(criminal)

def display_criminal(criminal):
    """Helper function to display a single criminal's details."""
    print(f"\n--- {criminal['name']} ({criminal['alias']}) ---")
    print(f"ID: {criminal['id']}")
    print(f"Physical: {criminal['physical']['height']}ft, {criminal['physical']['weight']}lbs, "
          f"{criminal['physical']['hair']} hair, {criminal['physical']['eyes']} eyes")
    print(f"Abilities: {', '.join(criminal['abilities'])}")
    print(f"Threat Level: {criminal['threat_level']}/10")
    print(f"Status: {criminal['status']}")
    print(f"Last Seen: {criminal['last_seen']}")
    print(f"Associates: {', '.join(criminal['associates'])}")
    print(f"Recent Crimes: {', '.join(criminal['recent_crimes'])}")

# Knightfall Protocol enhancements
def analyze_collaborations():
    """Analyze potential collaborations between criminals."""
    print("\n===== POTENTIAL COLLABORATIONS =====")
    
    potential_collaborations = []
    
    # Look for criminals who might be working together
    for i, criminal1 in enumerate(criminals):
        for criminal2 in criminals[i+1:]:
            score = 0
            reasons = []
            
            # Check for explicit association
            if criminal1["name"] in criminal2["associates"] or criminal2["name"] in criminal1["associates"]:
                score += 5
                reasons.append("Known associates")
            
            # Check for same location
            if criminal1["last_seen"] == criminal2["last_seen"]:
                score += 3
                reasons.append(f"Both last seen at {criminal1['last_seen']}")
            
            # Check for similar abilities
            common_abilities = set(criminal1["abilities"]).intersection(set(criminal2["abilities"]))
            if common_abilities:
                score += len(common_abilities)
                reasons.append(f"Shared abilities: {', '.join(common_abilities)}")
            
            # Check for similar recent crimes
            common_crimes = set(criminal1["recent_crimes"]).intersection(set(criminal2["recent_crimes"]))
            if common_crimes:
                score += len(common_crimes) * 2
                reasons.append(f"Involved in same crimes: {', '.join(common_crimes)}")
            
            # If score is significant, add to potential collaborations
            if score >= 3:
                potential_collaborations.append({
                    "criminals": [criminal1["name"], criminal2["name"]],
                    "score": score,
                    "reasons": reasons
                })
    
    # Sort collaborations by score
    potential_collaborations.sort(key=lambda x: x["score"], reverse=True)
    
    # Display results
    if potential_collaborations:
        print(f"Detected {len(potential_collaborations)} potential criminal collaborations:")
        for collab in potential_collaborations:
            print(f"\n{collab['criminals'][0]} and {collab['criminals'][1]}")
            print(f"Collaboration Likelihood: {collab['score']}/10")
            print(f"Evidence: {', '.join(collab['reasons'])}")
    else:
        print("No significant potential collaborations detected.")

def display_threat_map():
    """Display a simple ASCII threat map of Gotham City."""
    print("\n===== GOTHAM CITY THREAT MAP =====")
    
    # Define Gotham areas
    areas = [
        "Amusement Mile", "Arkham Asylum", "Blackgate Prison",
        "Diamond District", "East End", "Financial District",
        "Gotham Heights", "Iceberg Lounge", "Robinson Park",
        "Wayne Tower", "GCPD HQ", "Chinatown"
    ]
    
    # Create a threat mapping for each area
    threat_map = {}
    for area in areas:
        # Count criminals in this area
        criminals_here = [c for c in criminals if c["last_seen"] == area]
        
        # Calculate area threat level based on criminals present
        if criminals_here:
            threat = sum(c["threat_level"] for c in criminals_here) / len(criminals_here)
            criminals_list = [c["name"] for c in criminals_here]
        else:
            threat = random.randint(1, 4)  # Random low threat for areas with no known criminals
            criminals_list = []
        
        threat_map[area] = {
            "threat": threat,
            "criminals": criminals_list
        }
    
    # Display the map
    print("\n" + "=" * 50)
    print("         GOTHAM CITY - CRIMINAL THREAT LEVELS         ")
    print("=" * 50)
    
    # Display areas sorted by threat level
    sorted_areas = sorted(threat_map.items(), key=lambda x: x[1]["threat"], reverse=True)
    
    for area, data in sorted_areas:
        # Create a visual threat indicator
        threat = data["threat"]
        if threat >= 8:
            indicator = "🔴 HIGH ALERT"
        elif threat >= 5:
            indicator = "🟠 CAUTION"
        else:
            indicator = "🟢 MONITOR"
        
        # Display the area info
        print(f"\n{area}: {indicator} (Threat Level: {threat:.1f}/10)")
        
        if data["criminals"]:
            print(f"Known criminals: {', '.join(data['criminals'])}")
        else:
            print("No known criminals in this area.")
    
    print("\n" + "=" * 50)
    print("Plan patrol routes accordingly. Focus on high-threat areas.")
    print("=" * 50)

# Main menu function
def main_menu():
    """Display the main menu and handle user input."""
    print("\n===== BATCOMPUTER: CRIMINAL DATABASE =====")
    print("1. Add New Criminal")
    print("2. Search for Criminal")
    print("3. Assess Threat Level")
    print("4. Sort Criminals")
    print("5. Display All Criminals")
    print("6. Analyze Potential Collaborations (Knightfall)")
    print("7. Display Gotham Threat Map (Knightfall)")
    print("8. Exit")
    
    choice = input("\nEnter your choice (1-8): ")
    
    if choice == '1':
        add_criminal()
    elif choice == '2':
        search_criminal()
    elif choice == '3':
        assess_threat()
    elif choice == '4':
        sort_criminals()
    elif choice == '5':
        display_criminals()
    elif choice == '6':
        analyze_collaborations()
    elif choice == '7':
        display_threat_map()
    elif choice == '8':
        print("\nExiting Batcomputer. Stay vigilant, Batman.")
        return False
    else:
        print("\nInvalid choice. Please try again.")
    
    return True

def main():
    """Main function to run the Batcomputer Criminal Database."""
    print("\n" + "=" * 50)
    print("        BATCOMPUTER: CRIMINAL DATABASE v2.0        ")
    print("=" * 50)
    print("Initializing database...")
    
    # Load database if it exists (Knightfall Protocol)
    if os.path.exists("criminals.json"):
        load_database()
    else:
        print("No existing database found. Starting with sample data.")
    
    running = True
    while running:
        running = main_menu()
    
    # Save on exit
    save_database()

if __name__ == "__main__":
    main()
