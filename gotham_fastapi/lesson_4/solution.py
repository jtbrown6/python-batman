#!/usr/bin/env python3
"""
Gotham Protectors System - Complete Solution
----------------------------
A fully implemented object-oriented system to model Batman, his allies,
and their interactions with Gotham's villains.
Includes Knightfall Protocol enhancements with design patterns.
"""
import random
import time
import json
import os
from abc import ABC, abstractmethod

# Base Character class
class Character:
    """Base class for all characters in Gotham City."""
    
    def __init__(self, name, abilities=None):
        self.name = name
        self.abilities = abilities or []
        self.health = 100
        self.current_location = "Unknown"
    
    def move_to(self, location):
        """Move character to a new location."""
        self.current_location = location
        return f"{self.name} moved to {location}."
    
    def use_ability(self, ability_name):
        """Use one of the character's abilities."""
        if ability_name in self.abilities:
            return f"{self.name} used {ability_name}!"
        return f"{self.name} doesn't have the ability: {ability_name}."
    
    def __str__(self):
        """String representation of the character."""
        return f"{self.name} (Health: {self.health})"
    
    def __repr__(self):
        """Detailed representation of the character."""
        return f"{self.__class__.__name__}(name='{self.name}', abilities={self.abilities})"

# Hero class hierarchy
class Hero(Character):
    """Base class for all heroes in Gotham City."""
    
    def __init__(self, name, secret_identity, abilities=None):
        super().__init__(name, abilities)
        self._secret_identity = secret_identity  # Protected attribute
        self.is_patrolling = False
        self.villains_captured = []
        self.trusted_allies = ["Alfred Pennyworth", "Oracle", "Commissioner Gordon"]
    
    def reveal_identity(self, to_person):
        """Reveal secret identity only to trusted allies."""
        if to_person in self.trusted_allies:
            return f"{self.name} reveals to {to_person}: I am {self._secret_identity}."
        return f"{self.name}: My identity remains a secret, {to_person}."
    
    def patrol(self, location):
        """Patrol a specific location in Gotham."""
        self.move_to(location)
        self.is_patrolling = True
        return f"{self.name} is now patrolling {location}."
    
    def fight(self, villain):
        """Fight a villain with a chance of success."""
        print(f"{self.name} is fighting {villain.name}!")
        
        # Calculate success chance
        success_chance = 70  # Base chance
        
        # Bonus for abilities that counter villain weaknesses
        if set(self.abilities).intersection(villain.weaknesses):
            bonus = 20
            print(f"{self.name}'s abilities exploit {villain.name}'s weaknesses. +{bonus}% chance!")
            success_chance += bonus
        
        # Roll for success
        roll = random.randint(1, 100)
        print(f"Success chance: {success_chance}%, Roll: {roll}")
        
        if roll <= success_chance:
            villain.health -= 30
            
            if villain.health <= 0:
                return self.capture(villain)
            
            return f"{self.name} won the fight against {villain.name}!"
        else:
            self.health -= 20
            return f"{villain.name} got away after injuring {self.name}!"
    
    def capture(self, villain):
        """Capture a defeated villain."""
        if villain not in self.villains_captured and villain.health <= 0:
            villain.is_captured = True
            self.villains_captured.append(villain)
            return f"{self.name} has captured {villain.name} and is taking them to Arkham Asylum!"
        elif villain in self.villains_captured:
            return f"{villain.name} is already captured."
        else:
            return f"{villain.name} is still at large."
    
    @property
    def identity(self):
        """Property to protect the secret identity."""
        return "That information is protected."
    
    @property
    def captured_count(self):
        """Get the number of villains captured."""
        return len(self.villains_captured)

class BatFamily(Hero):
    """Members of the Bat-Family who share Batman's resources."""
    
    def __init__(self, name, secret_identity, abilities=None, mentor="Batman"):
        super().__init__(name, secret_identity, abilities)
        self.mentor = mentor
        self.base = "Batcave"
        self.gadgets = []
    
    def add_gadget(self, gadget):
        """Add a gadget to the hero's inventory."""
        self.gadgets.append(gadget)
        return f"{self.name} now has access to: {gadget}"
    
    def return_to_base(self):
        """Return to the Batcave."""
        return self.move_to(self.base)
    
    def use_gadget(self, gadget_name, target=None):
        """Use a gadget against a target."""
        if gadget_name in self.gadgets:
            target_msg = f" against {target.name}" if target else ""
            return f"{self.name} used {gadget_name}{target_msg}!"
        return f"{self.name} doesn't have {gadget_name}."

class Batman(BatFamily):
    """The Dark Knight himself."""
    
    def __init__(self):
        super().__init__(
            "Batman", 
            "Bruce Wayne",
            ["Detective Skills", "Martial Arts", "Intimidation", "Stealth", "Combat"]
        )
        self.gadgets = ["Batarang", "Grappling Hook", "Smoke Pellets", "Batclaw", "Batmobile Remote"]
        # Batman trusts his closest allies with his identity
        self.trusted_allies.extend(["Robin", "Nightwing", "Batgirl"])
        
        # Special attribute only available to Batman
        self.__bat_computer_password = "alfred1939"  # Strongly private
    
    def detective_mode(self, crime_scene):
        """Analyze a crime scene for clues."""
        return f"Batman uses his detective skills to analyze {crime_scene}. Several clues were found."
    
    def intimidate(self, target):
        """Intimidate a target for information."""
        success_chance = 90  # Batman is very intimidating
        roll = random.randint(1, 100)
        
        if roll <= success_chance:
            return f"Batman successfully intimidated {target} into providing information."
        else:
            return f"{target} refused to talk, even to Batman."
    
    # Override the fight method to demonstrate Batman's superior combat skills
    def fight(self, villain):
        print("Batman utilizes his superior combat training...")
        # First use the parent class fight method
        result = super().fight(villain)
        
        # Batman has special gadgets for specific villains
        if villain.name in ["Joker", "Riddler", "Penguin"] and villain.health > 0:
            specific_gadget = f"Anti-{villain.name} Device"
            print(f"Batman uses his {specific_gadget}!")
            villain.health -= 20
            
            if villain.health <= 0:
                return self.capture(villain)
            
            result += f" Batman used his {specific_gadget} for additional damage!"
            
        return result

class Robin(BatFamily):
    """Batman's sidekick."""
    
    def __init__(self, secret_identity="Tim Drake"):
        super().__init__(
            "Robin", 
            secret_identity,
            ["Acrobatics", "Bo Staff", "Combat", "Computer Skills"]
        )
        self.gadgets = ["Bo Staff", "Robin's Shuriken", "Grappling Hook"]
    
    def acrobatic_move(self):
        """Perform an acrobatic maneuver."""
        return "Robin performs an impressive acrobatic flip!"

class Nightwing(BatFamily):
    """Batman's former sidekick who became a hero in his own right."""
    
    def __init__(self):
        super().__init__(
            "Nightwing", 
            "Dick Grayson",
            ["Acrobatics", "Escrima Sticks", "Combat", "Leadership"]
        )
        self.gadgets = ["Escrima Sticks", "Wingdings", "Grappling Gun"]
        self.base = "Blüdhaven" # Nightwing operates in a different city
    
    def team_lead(self, team):
        """Lead a team of heroes."""
        return f"Nightwing takes charge, organizing {team} for a coordinated attack!"

# Villain class hierarchy
class Villain(Character):
    """Base class for all villains in Gotham City."""
    
    def __init__(self, name, abilities=None, weaknesses=None):
        super().__init__(name, abilities)
        self.is_captured = False
        self.crimes_committed = 0
        self.weaknesses = weaknesses or []
    
    def commit_crime(self, location, crime_type):
        """Commit a crime in a specific location."""
        if not self.is_captured:
            self.move_to(location)
            self.crimes_committed += 1
            return f"{self.name} committed {crime_type} in {location}!"
        return f"{self.name} is currently captured and cannot commit crimes."
    
    def escape(self):
        """Escape from captivity."""
        if self.is_captured:
            self.is_captured = False
            self.health = 50  # Reduced health after escape
            return f"{self.name} has escaped custody!"
        return f"{self.name} is already free."
    
    @abstractmethod
    def scheme(self):
        """Each villain has a unique scheme."""
        pass

class Joker(Villain):
    """Batman's arch-nemesis."""
    
    def __init__(self):
        super().__init__(
            "Joker",
            ["Chemical Expertise", "Psychological Manipulation", "Improvised Weapons"],
            ["Detective Skills", "Intimidation"]
        )
    
    def scheme(self):
        """Joker's unique scheme."""
        schemes = [
            "planning to poison Gotham's water supply with Joker toxin",
            "setting up an elaborate trap for Batman involving explosive teddy bears",
            "organizing a breakout at Arkham Asylum",
            "planning to assassinate the mayor during a public event"
        ]
        return f"The Joker is {random.choice(schemes)}."
    
    def laugh(self):
        """Joker's iconic laugh."""
        return "The Joker lets out a maniacal laugh: HAHAHAHAHAHAHA!"

class Riddler(Villain):
    """The puzzle-obsessed villain."""
    
    def __init__(self):
        super().__init__(
            "Riddler",
            ["Genius Intellect", "Puzzle Design", "Engineering"],
            ["Combat", "Intimidation"]
        )
    
    def scheme(self):
        """Riddler's unique scheme."""
        schemes = [
            "creating an elaborate death maze for Batman",
            "hacking into Gotham's traffic system to spell out a riddle",
            "kidnapping a prominent citizen as part of a complex puzzle",
            "planting riddle-based bombs throughout the city"
        ]
        return f"The Riddler is {random.choice(schemes)}."
    
    def pose_riddle(self):
        """Pose a riddle."""
        riddles = [
            "What has a head and a tail, but no body?",
            "The more you take, the more you leave behind. What am I?",
            "What gets wetter and wetter the more it dries?",
            "What can travel around the world while staying in a corner?"
        ]
        return f"Riddler: '{random.choice(riddles)}'"

class Penguin(Villain):
    """The sophisticated crime boss."""
    
    def __init__(self):
        super().__init__(
            "Penguin",
            ["Criminal Mastermind", "Weapons Trafficking", "Business Operations"],
            ["Acrobatics", "Stealth"]
        )
    
    def scheme(self):
        """Penguin's unique scheme."""
        schemes = [
            "running a smuggling operation through his Iceberg Lounge",
            "planning a heist of a rare bird exhibit",
            "laundering money through his legitimate businesses",
            "extorting Gotham's elite with blackmail"
        ]
        return f"The Penguin is {random.choice(schemes)}."
    
    def call_henchmen(self):
        """Call for henchmen support."""
        return "The Penguin calls in his umbrella-wielding henchmen for backup!"

# Knightfall Protocol Enhancements
# Observer Pattern for the Bat-Signal
class BatSignalObserver(ABC):
    """Interface for objects that can observe the Bat-Signal."""
    
    @abstractmethod
    def update(self, crime_type, location):
        """Method called when the Bat-Signal is activated."""
        pass

class BatSignal:
    """The Bat-Signal that alerts Batman and his allies."""
    
    def __init__(self):
        self._observers = []
        self._is_active = False
    
    def register(self, observer):
        """Register an observer for signal notifications."""
        if observer not in self._observers:
            self._observers.append(observer)
            return f"{observer.name} is now monitoring the Bat-Signal."
        return f"{observer.name} is already monitoring the Bat-Signal."
    
    def unregister(self, observer):
        """Unregister an observer from signal notifications."""
        if observer in self._observers:
            self._observers.remove(observer)
            return f"{observer.name} is no longer monitoring the Bat-Signal."
        return f"{observer.name} wasn't monitoring the Bat-Signal."
    
    def notify_all(self, crime_type, location):
        """Notify all observers of a signal activation."""
        for observer in self._observers:
            observer.update(crime_type, location)
    
    def activate(self, crime_type, location):
        """Activate the Bat-Signal for a specific crime."""
        self._is_active = True
        print(f"\nBat-Signal activated for {crime_type} at {location}!")
        self.notify_all(crime_type, location)
    
    def deactivate(self):
        """Deactivate the Bat-Signal."""
        self._is_active = False
        print("\nBat-Signal deactivated.")

# Make Batman and other heroes observe the Bat-Signal
class BatSignalReceiver(BatFamily, BatSignalObserver):
    """A hero that can respond to the Bat-Signal."""
    
    def update(self, crime_type, location):
        """Respond to a Bat-Signal activation."""
        print(f"{self.name} received alert: {crime_type} at {location}")
        self.patrol(location)

# Strategy Pattern for Combat
class CombatStrategy(ABC):
    """Interface for different combat strategies."""
    
    @abstractmethod
    def execute(self, attacker, defender):
        """Execute the combat strategy."""
        pass

class StealthTakedown(CombatStrategy):
    """A silent, stealthy approach to combat."""
    
    def execute(self, attacker, defender):
        """Execute a stealth takedown."""
        success_chance = 90  # High chance of success
        
        if "Stealth" in attacker.abilities:
            success_chance += 5
        
        roll = random.randint(1, 100)
        
        if roll <= success_chance:
            defender.health -= 50  # Highly effective
            return f"{attacker.name} performed a silent takedown on {defender.name}!"
        else:
            return f"{attacker.name}'s stealth approach failed. {defender.name} is now alert!"

class DirectAssault(CombatStrategy):
    """A direct, confrontational approach to combat."""
    
    def execute(self, attacker, defender):
        """Execute a direct assault."""
        success_chance = 70
        
        if "Combat" in attacker.abilities:
            success_chance += 10
        
        roll = random.randint(1, 100)
        
        if roll <= success_chance:
            defender.health -= 30
            return f"{attacker.name} directly confronted and fought {defender.name}!"
        else:
            attacker.health -= 15
            return f"{defender.name} fought back and injured {attacker.name}!"

class GadgetAttack(CombatStrategy):
    """Using gadgets in combat."""
    
    def execute(self, attacker, defender):
        """Execute an attack using gadgets."""
        if not hasattr(attacker, 'gadgets') or not attacker.gadgets:
            return f"{attacker.name} doesn't have any gadgets to use!"
        
        gadget = random.choice(attacker.gadgets)
        success_chance = 80
        
        roll = random.randint(1, 100)
        
        if roll <= success_chance:
            defender.health -= 35
            return f"{attacker.name} used {gadget} against {defender.name} effectively!"
        else:
            return f"{attacker.name}'s attempt to use {gadget} against {defender.name} failed!"

# Make Batman and others use combat strategies
class StrategicCombatant(BatFamily):
    """A hero that can use different combat strategies."""
    
    def __init__(self, name, secret_identity, abilities=None, mentor="Batman"):
        super().__init__(name, secret_identity, abilities, mentor)
        self.combat_strategy = DirectAssault()  # Default strategy
    
    def set_combat_strategy(self, strategy):
        """Change the combat strategy."""
        self.combat_strategy = strategy
        return f"{self.name} changed combat strategy to {strategy.__class__.__name__}."
    
    def engage(self, villain):
        """Engage a villain using the current combat strategy."""
        return self.combat_strategy.execute(self, villain)

# Enhanced Batman with Strategy and Observer patterns
class EnhancedBatman(Batman, BatSignalObserver):
    """Batman with Knightfall Protocol enhancements."""
    
    def __init__(self):
        super().__init__()
        self.combat_strategies = {
            "stealth": StealthTakedown(),
            "direct": DirectAssault(),
            "gadget": GadgetAttack()
        }
        self.current_strategy = self.combat_strategies["direct"]
    
    def update(self, crime_type, location):
        """Respond to Bat-Signal."""
        print(f"Batman received alert: {crime_type} at {location}")
        
        # Choose appropriate strategy based on crime type
        if crime_type in ["Robbery", "Hostage Situation"]:
            self.current_strategy = self.combat_strategies["stealth"]
            print("Batman opts for a stealthy approach.")
        elif crime_type in ["Assault", "Gang Activity"]:
            self.current_strategy = self.combat_strategies["direct"]
            print("Batman prepares for direct confrontation.")
        else:
            self.current_strategy = self.combat_strategies["gadget"]
            print("Batman selects appropriate gadgets.")
        
        self.patrol(location)
    
    def engage(self, villain):
        """Engage a villain using the current strategy."""
        return self.current_strategy.execute(self, villain)

# Gotham City Management
class GothamCity:
    """Class to manage the state of Gotham City and interactions."""
    
    def __init__(self):
        self.locations = [
            "Batcave", "Wayne Manor", "Arkham Asylum", "GCPD", 
            "Downtown", "East End", "Diamond District", "Amusement Mile", 
            "Gotham Heights", "Iceberg Lounge"
        ]
        self.heroes = []
        self.villains = []
        self.crime_level = 5  # Scale of 1-10
        self.bat_signal = BatSignal()
    
    def add_character(self, character):
        """Add a character to the city."""
        if isinstance(character, Hero):
            self.heroes.append(character)
            # Register BatSignal observers
            if isinstance(character, BatSignalObserver):
                self.bat_signal.register(character)
            return f"{character.name} added to Gotham's heroes."
        elif isinstance(character, Villain):
            self.villains.append(character)
            return f"{character.name} added to Gotham's villains."
        return f"Unknown character type: {character.__class__.__name__}"
    
    def random_crime(self):
        """Generate a random crime in the city."""
        if not self.villains or all(v.is_captured for v in self.villains):
            return "All villains are currently captured. Gotham is safe... for now."
        
        available_villains = [v for v in self.villains if not v.is_captured]
        villain = random.choice(available_villains)
        
        crime_types = ["Robbery", "Assault", "Kidnapping", "Hostage Situation", "Gang Activity"]
        crime_type = random.choice(crime_types)
        
        location = random.choice(self.locations)
        
        result = villain.commit_crime(location, crime_type)
        
        # If crime level gets too high, activate the Bat-Signal
        self.crime_level += random.randint(1, 3)
        self.crime_level = min(10, self.crime_level)
        
        if self.crime_level >= 8:
            print(f"Crime level reaching critical: {self.crime_level}/10")
            self.bat_signal.activate(crime_type, location)
        
        return result
    
    def simulate_patrol(self):
        """Simulate heroes patrolling and encountering villains."""
        if not self.heroes:
            return "No heroes are currently protecting Gotham."
        
        results = []
        
        for hero in self.heroes:
            if not hasattr(hero, 'is_patrolling') or not hero.is_patrolling:
                results.append(f"{hero.name} is not on patrol.")
                continue
            
            location = hero.current_location
            villains_here = [v for v in self.villains 
                            if v.current_location == location and not v.is_captured]
            
            if not villains_here:
                results.append(f"{hero.name} patrols {location} but finds no criminal activity.")
                self.crime_level = max(1, self.crime_level - 1)  # Reduce crime level
                continue
            
            for villain in villains_here:
                if hasattr(hero, 'engage') and isinstance(hero, StrategicCombatant):
                    # Use strategy pattern for combat
                    result = hero.engage(villain)
                    results.append(result)
                else:
                    # Standard combat
                    result = hero.fight(villain)
                    results.append(result)
                
                # If villain captured, reduce crime level
                if villain.is_captured:
                    self.crime_level = max(1, self.crime_level - 2)
                    
                    # Deactivate Bat-Signal if crime level drops
                    if self.crime_level < 5:
                        self.bat_signal.deactivate()
        
        # City status after patrol
        results.append(f"Current crime level in Gotham: {self.crime_level}/10")
        return "\n".join(results)
    
    def status_report(self):
        """Generate a status report for Gotham City."""
        report = ["\n===== GOTHAM CITY STATUS REPORT ====="]
        
        # Heroes status
        report.append("\nHEROES:")
        for hero in self.heroes:
            status = "On patrol" if getattr(hero, 'is_patrolling', False) else "On standby"
            location = hero.current_location
            report.append(f"  {hero.name}: {status} at {location}, Health: {hero.health}/100")
            
            if hasattr(hero, 'villains_captured') and hero.villains_captured:
                captures = [v.name for v in hero.villains_captured]
                report.append(f"    Villains captured: {', '.join(captures)}")
        
        # Villains status
        report.append("\nVILLAINS:")
        for villain in self.villains:
            status = "Captured" if villain.is_captured else "At large"
            location = villain.current_location
            report.append(f"  {villain.name}: {status} at {location}, Health: {villain.health}/100")
            
            if not villain.is_captured:
                report.append(f"    Current scheme: {villain.scheme()}")
        
        # City status
        report.append(f"\nCrime Level: {self.crime_level}/10")
        if self.crime_level <= 3:
            report.append("Gotham is relatively peaceful.")
        elif self.crime_level <= 6:
            report.append("Gotham has moderate criminal activity.")
        else:
            report.append("Gotham is experiencing high levels of crime!")
        
        report.append("=" * 37)
        return "\n".join(report)
    
    # Serialization methods (Knightfall Protocol)
    def save_state(self, filename="gotham_state.json"):
        """Save the current state of Gotham City."""
        state = {
            "crime_level": self.crime_level,
            "heroes": [],
            "villains": []
        }
        
        # We can't directly serialize objects, so we extract their data
        for hero in self.heroes:
            hero_data = {
                "name": hero.name,
                "secret_identity": getattr(hero, '_secret_identity', "Unknown"),
                "health": hero.health,
                "location": hero.current_location,
                "is_patrolling": getattr(hero, 'is_patrolling', False),
                "abilities": hero.abilities,
                "type": hero.__class__.__name__
            }
            state["heroes"].append(hero_data)
        
        for villain in self.villains:
            villain_data = {
                "name": villain.name,
                "health": villain.health,
                "location": villain.current_location,
                "is_captured": villain.is_captured,
                "abilities": villain.abilities,
                "weaknesses": villain.weaknesses,
                "type": villain.__class__.__name__
            }
            state["villains"].append(villain_data)
        
        with open(filename, 'w') as f:
            json.dump(state, f, indent=4)
        
        return f"Gotham City state saved to {filename}."
    
    def load_state(self, filename="gotham_state.json"):
        """Load a saved state of Gotham City."""
        if not os.path.exists(filename):
            return f"No saved state found at {filename}."
        
        with open(filename, 'r') as f:
            state = json.load(f)
        
        self.crime_level = state["crime_level"]
        self.heroes = []
        self.villains = []
        
        # Re-create heroes based on their types
        for hero_data in state["heroes"]:
            if hero_data["type"] == "Batman":
                hero = Batman()
            elif hero_data["type"] == "Robin":
                hero = Robin(hero_data["secret_identity"])
            elif hero_data["type"] == "Nightwing":
                hero = Nightwing()
            elif hero_data["type"] == "EnhancedBatman":
                hero = EnhancedBatman()
            else:
                # Generic hero
                hero = BatFamily(
                    hero_data["name"],
                    hero_data["secret_identity"],
                    hero_data["abilities"]
                )
            
            # Restore state
            hero.health = hero_data["health"]
            hero.current_location = hero_data["location"]
            hero.is_patrolling = hero_data["is_patrolling"]
            
            self.add_character(hero)
        
        # Re-create villains based on their types
        for villain_data in state["villains"]:
            if villain_data["type"] == "Joker":
                villain = Joker()
            elif villain_data["type"] == "Riddler":
                villain = Riddler()
            elif villain_data["type"] == "Penguin":
                villain = Penguin()
            else:
                # Generic villain
                class GenericVillain(Villain):
                    def scheme(self):
                        return f"{self.name} is planning something nefarious!"
                
                villain = GenericVillain(
                    villain_data["name"],
                    villain_data["abilities"],
                    villain_data["weaknesses"]
                )
            
            # Restore state
            villain.health = villain_data["health"]
            villain.current_location = villain_data["location"]
            villain.is_captured = villain_data["is_captured"]
            
            self.add_character(villain)
        
        return f"Gotham City state loaded from {filename}."

# Command-line interface for Knightfall Protocol
def run_gotham_cli():
    """Run a command-line interface to interact with Gotham City."""
    gotham = GothamCity()
    
    # Create characters
    batman = EnhancedBatman()
    robin = Robin()
    nightwing = Nightwing()
    
    joker = Joker()
    riddler = Riddler()
    penguin = Penguin()
    
    # Add characters to Gotham
    for character in [batman, robin, nightwing, joker, riddler, penguin]:
        gotham.add_character(character)
    
    print("\n===== WELCOME TO GOTHAM CITY =====")
    print("The command-line interface for the Gotham Protectors System")
    
    running = True
    while running:
        print("\nCommand Menu:")
        print("1. Show Gotham Status")
        print("2. Send Hero on Patrol")
        print("3. Simulate Random Crime")
        print("4. Simulate Patrol Results")
        print("5. Activate Bat-Signal")
        print("6. Change Combat Strategy")
        print("7. Save Gotham State")
        print("8. Load Gotham State")
        print("9. Detailed Character Info")
        print("0. Exit System")
        
        choice = input("\nEnter your choice (0-9): ")
        
        if choice == '1':
            print(gotham.status_report())
        
        elif choice == '2':
            # Show available heroes
            print("\nAvailable Heroes:")
            for i, hero in enumerate(gotham.heroes, 1):
                print(f"{i}. {hero.name}")
            
            try:
                hero_idx = int(input("Select hero (number): ")) - 1
                if 0 <= hero_idx < len(gotham.heroes):
                    # Show available locations
                    print("\nLocations in Gotham:")
                    for i, location in enumerate(gotham.locations, 1):
                        print(f"{i}. {location}")
                    
                    loc_idx = int(input("Select patrol location (number): ")) - 1
                    if 0 <= loc_idx < len(gotham.locations):
                        hero = gotham.heroes[hero_idx]
                        location = gotham.locations[loc_idx]
                        result = hero.patrol(location)
                        print(result)
                    else:
                        print("Invalid location selection.")
                else:
                    print("Invalid hero selection.")
            except ValueError:
                print("Please enter valid numbers.")
        
        elif choice == '3':
            result = gotham.random_crime()
            print(result)
        
        elif choice == '4':
            result = gotham.simulate_patrol()
            print(result)
        
        elif choice == '5':
            # Show available crime types
            crime_types = ["Robbery", "Assault", "Kidnapping", "Hostage Situation", "Gang Activity"]
            print("\nCrime Types:")
            for i, crime_type in enumerate(crime_types, 1):
                print(f"{i}. {crime_type}")
            
            try:
                crime_idx = int(input("Select crime type (number): ")) - 1
                if 0 <= crime_idx < len(crime_types):
                    # Show available locations
                    print("\nLocations in Gotham:")
                    for i, location in enumerate(gotham.locations, 1):
                        print(f"{i}. {location}")
                    
                    loc_idx = int(input("Select location (number): ")) - 1
                    if 0 <= loc_idx < len(gotham.locations):
                        crime_type = crime_types[crime_idx]
                        location = gotham.locations[loc_idx]
                        gotham.bat_signal.activate(crime_type, location)
                    else:
                        print("Invalid location selection.")
                else:
                    print("Invalid crime type selection.")
            except ValueError:
                print("Please enter valid numbers.")
        
        elif choice == '6':
            # Show available heroes
            strategic_heroes = [hero for hero in gotham.heroes 
                               if isinstance(hero, EnhancedBatman)]
            
            if not strategic_heroes:
                print("No heroes with switchable combat strategies available.")
                continue
            
            print("\nHeroes with Switchable Combat Strategies:")
            for i, hero in enumerate(strategic_heroes, 1):
                print(f"{i}. {hero.name}")
            
            try:
                hero_idx = int(input("Select hero (number): ")) - 1
                if 0 <= hero_idx < len(strategic_heroes):
                    hero = strategic_heroes[hero_idx]
                    
                    # Show available strategies
                    strategies = ["Stealth Takedown", "Direct Assault", "Gadget Attack"]
                    print("\nAvailable Strategies:")
                    for i, strategy in enumerate(strategies, 1):
                        print(f"{i}. {strategy}")
                    
                    strategy_idx = int(input("Select strategy (number): ")) - 1
                    if 0 <= strategy_idx < len(strategies):
                        if strategy_idx == 0:
                            hero.current_strategy = StealthTakedown()
                        elif strategy_idx == 1:
                            hero.current_strategy = DirectAssault()
                        else:
                            hero.current_strategy = GadgetAttack()
                        
                        print(f"{hero.name} switched to {strategies[strategy_idx]} strategy.")
                    else:
                        print("Invalid strategy selection.")
                else:
                    print("Invalid hero selection.")
            except ValueError:
                print("Please enter valid numbers.")
        
        elif choice == '7':
            filename = input("Enter filename (default: gotham_state.json): ") or "gotham_state.json"
            result = gotham.save_state(filename)
            print(result)
        
        elif choice == '8':
            filename = input("Enter filename (default: gotham_state.json): ") or "gotham_state.json"
            result = gotham.load_state(filename)
            print(result)
        
        elif choice == '9':
            # Show all characters
            all_characters = gotham.heroes + gotham.villains
            print("\nAll Characters:")
            for i, character in enumerate(all_characters, 1):
                print(f"{i}. {character.name}")
            
            try:
                char_idx = int(input("Select character (number): ")) - 1
                if 0 <= char_idx < len(all_characters):
                    character = all_characters[char_idx]
                    print(f"\n--- {character.name} Details ---")
                    print(f"Type: {character.__class__.__name__}")
                    print(f"Health: {character.health}/100")
                    print(f"Location: {character.current_location}")
                    print(f"Abilities: {', '.join(character.abilities)}")
                    
                    if isinstance(character, Hero):
                        print(f"Secret Identity: Protected")
                        print(f"Status: {'On patrol' if character.is_patrolling else 'On standby'}")
                        print(f"Villains Captured: {character.captured_count}")
                        
                        if hasattr(character, 'gadgets'):
                            print(f"Gadgets: {', '.join(character.gadgets)}")
                    
                    if isinstance(character, Villain):
                        print(f"Status: {'Captured' if character.is_captured else 'At large'}")
                        print(f"Weaknesses: {', '.join(character.weaknesses)}")
                        print(f"Crimes Committed: {character.crimes_committed}")
                        
                        if not character.is_captured:
                            print(f"Current Scheme: {character.scheme()}")
                else:
                    print("Invalid character selection.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == '0':
            print("\nExiting Gotham Protectors System. Stay vigilant!")
            running = False
        
        else:
            print("Invalid choice. Please try again.")

# Helper functions
def print_separator():
    """Print a separator line."""
    print("-" * 50)

def demonstrate_inheritance():
    """Demonstrate inheritance in the Gotham Protectors System."""
    print("\n===== DEMONSTRATING INHERITANCE =====")
    
    # Create characters
    batman = Batman()
    robin = Robin()
    joker = Joker()
    
    # Show character hierarchy
    print("Batman is a BatFamily, which is a Hero, which is a Character.")
    print(f"Batman's parent classes: {Batman.__mro__}")
    
    # Demonstrate inherited methods
    print("\nDemonstrating inherited methods:")
    print(batman.move_to("Downtown"))  # From Character
    print(batman.patrol("East End"))    # From Hero
    print(batman.add_gadget("Batcomputer Remote"))  # From BatFamily
    
    # Demonstrate method overriding
    print("\nDemonstrating method overriding:")
    print("Standard fight method:")
    robin.health = 100
    joker.health = 100
    print(robin.fight(joker))
    
    print("\nOverridden fight method:")
    batman.health = 100
    joker.health = 100
    print(batman.fight(joker))
    
    print_separator()

def demonstrate_polymorphism():
    """Demonstrate polymorphism in the Gotham Protectors System."""
    print("\n===== DEMONSTRATING POLYMORPHISM =====")
    
    # Create villains
    joker = Joker()
    riddler = Riddler()
    penguin = Penguin()
    
    # Store them in a list of the base class
    villains = [joker, riddler, penguin]
    
    # Call the same method on each, which will behave differently
    print("Each villain schemes differently:")
    for villain in villains:
        print(f"{villain.name}: {villain.scheme()}")
    
    # Demonstrate polymorphism with hero combat strategies
    batman = EnhancedBatman()
    enemy = Joker()
    enemy.health = 100
    
    print("\nBatman using different combat strategies:")
    
    # Store different strategies
    strategies = {
        "Stealth": StealthTakedown(),
        "Direct": DirectAssault(),
        "Gadget": GadgetAttack()
    }
    
    # Use each strategy polymorphically
    for name, strategy in strategies.items():
        enemy.health = 100  # Reset enemy health
        batman.current_strategy = strategy
        print(f"Using {name} strategy: {batman.engage(enemy)}")
    
    print_separator()

def demonstrate_encapsulation():
    """Demonstrate encapsulation in the Gotham Protectors System."""
    print("\n===== DEMONSTRATING ENCAPSULATION =====")
    
    batman = Batman()
    
    # Public methods and attributes
    print("Public interface:")
    print(f"Name: {batman.name}")
    print(f"Current location: {batman.current_location}")
    
    # Protected attributes (convention with single underscore)
    print("\nAccessing protected attribute (not recommended):")
    print(f"Secret identity (protected): {batman._secret_identity}")
    
    # Property access
    print("\nUsing property to access protected data:")
    print(f"Identity property: {batman.identity}")
    
    # Controlled access through methods
    print("\nControlled access through methods:")
    print(batman.reveal_identity("Joker"))
    print(batman.reveal_identity("Alfred Pennyworth"))
    
    # Private attribute (double underscore)
    print("\nAttempting to access private attribute:")
    try:
        # This will raise an AttributeError
        print(batman.__bat_computer_password)
    except AttributeError as e:
        print(f"Error: {e}")
    
    # Name mangling allows access if you know the implementation
    print("\nName mangling doesn't provide true privacy:")
    print(f"Accessing mangled name: {batman._Batman__bat_computer_password}")
    
    print_separator()

def main():
    """Main function to demonstrate the Gotham Protectors System."""
    print("\n===== GOTHAM PROTECTORS SYSTEM =====")
    
    # Demonstrate key OOP concepts
    demonstrate_inheritance()
    demonstrate_polymorphism()
    demonstrate_encapsulation()
    
    # Ask if user wants to run the interactive CLI
    choice = input("\nWould you like to run the interactive Gotham City CLI? (y/n): ")
    if choice.lower() == 'y':
        run_gotham_cli()
    else:
        print("\nThank you for using the Gotham Protectors System.")
        print("Remember: 'The night is darkest just before the dawn.'")

if __name__ == "__main__":
    main()
