# Bruce Wayne's Journal: Gotham Protectors System

## Thought Process for Object-Oriented Design

When designing a system to model the characters and interactions in Gotham City, I approached it as I would any crime-fighting mission: with careful planning and a clear hierarchy.

### 1. Class Hierarchy Design

**Thought process:**
- Need a base class that captures what all characters in Gotham have in common
- Heroes and villains share some attributes but differ in behavior
- Specific characters like Batman or Joker need specialized implementations
- The system should model real interactions like combat and investigations

**Solution approach:**
- Create a base `Character` class with common attributes (name, abilities)
- Derive `Hero` and `Villain` classes with their specific behaviors
- Create concrete classes for specific characters with their unique traits
- Design classes to interact through well-defined methods

```
Character (base class)
├── Hero (derived class)
│   ├── Batman
│   ├── Robin
│   └── Batgirl
└── Villain (derived class)
    ├── Joker
    ├── Penguin
    └── Riddler
```

### 2. Encapsulation for Secret Identities

**Thought process:**
- Secret identities are critical and must be protected
- Only certain methods should have access to this private information
- Need a way to securely access and modify protected attributes

**Solution approach:**
- Use private attributes with underscore prefix (`_secret_identity`)
- Implement getter methods with authorization checks
- Use property decorators for controlled access to attributes
- Consider using double underscore for attributes that should truly be hidden

```python
class Hero(Character):
    def __init__(self, name, secret_identity):
        super().__init__(name)
        self._secret_identity = secret_identity  # Protected attribute
    
    def reveal_identity(self, to_person):
        # Only reveal to trusted allies
        if to_person in self.trusted_allies:
            return self._secret_identity
        return "My identity remains a secret."
```

### 3. Inheritance for Specialized Skills

**Thought process:**
- Different heroes have different abilities and equipment
- Common hero behaviors should be shared in parent classes
- Specialized behaviors should override general ones when needed

**Solution approach:**
- Define basic methods in the `Hero` class (patrol, fight, etc.)
- Override methods in specific classes like `Batman` to specialize behavior
- Use `super()` to extend rather than completely replace parent methods

```python
class Batman(Hero):
    def __init__(self):
        super().__init__("Batman", "Bruce Wayne")
        self.gadgets = ["Batarang", "Grappling Hook", "Smoke Pellets"]
    
    def fight(self, opponent):
        # Batman fights with more effectiveness
        result = super().fight(opponent)  # Call the parent method
        if self.has_gadget_for(opponent):
            return f"{result} Batman used a specialized gadget for increased effect!"
        return result
```

### 4. Polymorphism for Varied Behaviors

**Thought process:**
- Different character types should respond uniquely to the same action
- Want to be able to treat different objects through a common interface
- Need to support different "strategies" for actions like combat or investigation

**Solution approach:**
- Define common method signatures in the base classes
- Implement the methods differently in each derived class
- Use abstract methods when appropriate to enforce implementation

```python
# In each villain class
def scheme(self):
    # Each villain schemes differently
    pass

class Joker(Villain):
    def scheme(self):
        return "Planning chaos and mayhem across Gotham!"

class Riddler(Villain):
    def scheme(self):
        return "Designing a puzzling death trap for Batman!"
```

### 5. Managing Interactions

**Thought process:**
- Need a system to coordinate interactions between characters
- Want to model the city itself as a containing environment
- Need to track the state of characters (location, health, etc.)

**Solution approach:**
- Create a `GothamCity` class to manage the overall simulation
- Implement methods for encounters between heroes and villains
- Keep track of character states and locations
- Provide methods to simulate time passing and events occurring

```python
class GothamCity:
    def __init__(self):
        self.locations = ["Arkham Asylum", "Batcave", "GCPD", "Downtown", "East End"]
        self.heroes = []
        self.villains = []
        self.crime_level = 5  # Scale of 1-10
    
    def add_character(self, character):
        if isinstance(character, Hero):
            self.heroes.append(character)
        elif isinstance(character, Villain):
            self.villains.append(character)
    
    def simulate_patrol(self):
        # Simulate heroes patrolling and potentially encountering villains
        for hero in self.heroes:
            location = hero.current_location
            villains_here = [v for v in self.villains if v.current_location == location]
            
            for villain in villains_here:
                self.simulate_encounter(hero, villain)
```

## Implementation Hints

### Character Base Class:
```python
class Character:
    def __init__(self, name, abilities=None):
        self.name = name
        self.abilities = abilities or []
        self.health = 100
        self.current_location = "Unknown"
    
    def move_to(self, location):
        self.current_location = location
        return f"{self.name} moved to {location}"
    
    def use_ability(self, ability_name):
        if ability_name in self.abilities:
            return f"{self.name} used {ability_name}!"
        return f"{self.name} doesn't have that ability!"
```

### Hero Class:
```python
class Hero(Character):
    def __init__(self, name, secret_identity, abilities=None):
        super().__init__(name, abilities)
        self._secret_identity = secret_identity
        self.is_patrolling = False
        self.villains_captured = []
    
    def patrol(self, location):
        self.move_to(location)
        self.is_patrolling = True
        return f"{self.name} is now patrolling {location}"
    
    def fight(self, villain):
        # Simplified combat system
        success_chance = 70  # Base 70% chance to win
        if set(self.abilities).intersection(villain.weaknesses):
            success_chance += 20  # Bonus for having abilities that exploit weaknesses
        
        if random.randint(1, 100) <= success_chance:
            villain.health -= 30
            if villain.health <= 0:
                self.capture(villain)
                return f"{self.name} defeated and captured {villain.name}!"
            return f"{self.name} won the fight against {villain.name}!"
        else:
            self.health -= 20
            return f"{villain.name} got away after injuring {self.name}!"
```

### Villain Class:
```python
class Villain(Character):
    def __init__(self, name, abilities=None, weaknesses=None):
        super().__init__(name, abilities)
        self.is_captured = False
        self.crimes_committed = 0
        self.weaknesses = weaknesses or []
    
    def commit_crime(self, location, crime_type):
        if not self.is_captured:
            self.move_to(location)
            self.crimes_committed += 1
            return f"{self.name} committed {crime_type} in {location}!"
        return f"{self.name} is currently captured and cannot commit crimes."
    
    def escape(self):
        if self.is_captured:
            self.is_captured = False
            return f"{self.name} has escaped custody!"
        return f"{self.name} is already free."
```

### For the Knightfall Protocol (Push Harder Challenge)

#### Observer Pattern for the Bat-Signal:
```python
class BatSignal:
    def __init__(self):
        self._observers = []
        self._is_active = False
    
    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_all(self, crime_type, location):
        for observer in self._observers:
            observer.update(crime_type, location)
    
    def activate(self, crime_type, location):
        self._is_active = True
        print(f"Bat-Signal activated for {crime_type} at {location}!")
        self.notify_all(crime_type, location)
    
    def deactivate(self):
        self._is_active = False
        print("Bat-Signal deactivated.")


class BatSignalObserver:
    def update(self, crime_type, location):
        pass  # To be implemented by specific observers

class Batman(Hero, BatSignalObserver):
    # Other methods...
    
    def update(self, crime_type, location):
        print(f"Batman received alert: {crime_type} at {location}")
        self.patrol(location)
```

#### Strategy Pattern for Combat:
```python
class CombatStrategy:
    def execute(self, attacker, defender):
        pass  # Abstract method

class StealthTakedown(CombatStrategy):
    def execute(self, attacker, defender):
        success_chance = 90  # High chance of success
        if "Stealth" in attacker.abilities:
            success_chance += 5
        
        if random.randint(1, 100) <= success_chance:
            defender.health -= 50  # Highly effective
            return f"{attacker.name} performed a silent takedown on {defender.name}!"
        else:
            return f"{attacker.name}'s stealth approach failed. {defender.name} is now alert!"

class DirectAssault(CombatStrategy):
    def execute(self, attacker, defender):
        success_chance = 70
        if "Combat" in attacker.abilities:
            success_chance += 10
        
        if random.randint(1, 100) <= success_chance:
            defender.health -= 30
            return f"{attacker.name} directly confronted and fought {defender.name}!"
        else:
            attacker.health -= 15
            return f"{defender.name} fought back and injured {attacker.name}!"


class BatFamily(Hero):
    def __init__(self, name, secret_identity, abilities=None):
        super().__init__(name, secret_identity, abilities)
        self.combat_strategy = DirectAssault()  # Default strategy
    
    def set_combat_strategy(self, strategy):
        self.combat_strategy = strategy
    
    def engage(self, villain):
        return self.combat_strategy.execute(self, villain)
```

Remember: "The night is darkest just before the dawn. And I promise you, the dawn is coming."
