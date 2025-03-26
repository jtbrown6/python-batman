#!/usr/bin/env python3
"""
Batcomputer Criminal Database
----------------------------
Your mission: Create a criminal database system for Batman
to track Gotham's most wanted criminals.
"""

# TODO: Define your data structures to store criminal information
# Consider using dictionaries for each criminal with various attributes
# criminals = []  # You might use a list of dictionaries

# TODO: Function to add a new criminal to the database
def add_criminal():
    # Example implementation:
    # name = input("Enter criminal name: ")
    # aka = input("Enter alias (if any): ")
    # ...
    # Add the criminal to your data structure
    pass

# TODO: Function to search for criminals by name
def search_criminal():
    # Example implementation:
    # search_term = input("Enter search term: ")
    # Search your data structure and return matches
    pass

# TODO: Function to assess threat level
def assess_threat():
    # Example implementation:
    # name = input("Enter criminal name: ")
    # Find the criminal in your data structure
    # Calculate threat level based on various factors
    pass

# TODO: Function to sort criminals by different criteria
def sort_criminals():
    # Example implementation:
    # criterion = input("Sort by (name/threat/...): ")
    # Sort your data structure and display results
    pass

# TODO: Function to display all criminals
def display_criminals():
    # Display all criminals in a formatted way
    pass

# Main menu function
def main_menu():
    """Display the main menu and handle user input."""
    print("\n===== BATCOMPUTER: CRIMINAL DATABASE =====")
    print("1. Add New Criminal")
    print("2. Search for Criminal")
    print("3. Assess Threat Level")
    print("4. Sort Criminals")
    print("5. Display All Criminals")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ")
    
    # TODO: Handle the user's choice by calling the appropriate function
    if choice == '1':
        add_criminal()
    elif choice == '2':
        search_criminal()
    # Continue with the rest of the options...
    elif choice == '6':
        print("Exiting Batcomputer. Stay vigilant, Batman.")
        return False
    else:
        print("Invalid choice. Please try again.")
    
    return True

def main():
    # TODO: Initialize your database (perhaps load from a file for the Knightfall challenge)
    
    running = True
    while running:
        running = main_menu()

if __name__ == "__main__":
    main()
