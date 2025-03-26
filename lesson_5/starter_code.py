#!/usr/bin/env python3
"""
Batcomputer Criminal Database API
----------------------------
Your mission: Create a complete RESTful API for Batman's criminal database
using FastAPI.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Initialize the Batcomputer API
app = FastAPI(
    title="Batcomputer API",
    description="Access to Batman's criminal database and Gotham City information",
    version="1.0.0"
)

# TODO: Define a Pydantic model for Criminal
# class Criminal(BaseModel):
#     # Define the fields for a criminal record
#     pass

# Sample criminal database (in a real application, this would be a database)
criminals_db = [
    {"id": 1, "name": "Joker", "status": "At large", "threat_level": "Extreme", 
     "last_known_location": "Amusement Mile", "psycho_profile": "Psychopath with a theatrical flair"},
    {"id": 2, "name": "Penguin", "status": "In custody", "threat_level": "High", 
     "last_known_location": "Blackgate Prison", "psycho_profile": "Narcissistic with inferiority complex"},
    {"id": 3, "name": "Riddler", "status": "Unknown", "threat_level": "High", 
     "last_known_location": "Cyberspace", "psycho_profile": "Obsessive-compulsive with superiority complex"}
]

# Root endpoint
@app.get("/")
async def batcomputer_welcome():
    """Welcome message for the Batcomputer API."""
    return {"message": "Welcome to the Batcomputer. Authorize to proceed."}

# TODO: Implement GET endpoint to list all criminals
# @app.get("/criminals/")
# async def list_criminals():
#     pass

# TODO: Implement GET endpoint to retrieve a specific criminal by ID
# @app.get("/criminals/{criminal_id}")
# async def get_criminal(criminal_id: int):
#     pass

# TODO: Implement GET endpoint to search criminals by various parameters
# @app.get("/criminals/search")
# async def search_criminals(...):
#     pass

# TODO: Implement POST endpoint to add a new criminal
# @app.post("/criminals/", status_code=201)
# async def create_criminal(criminal: Criminal):
#     pass

# TODO: Implement PUT endpoint to update an existing criminal
# @app.put("/criminals/{criminal_id}")
# async def update_criminal(criminal_id: int, criminal: Criminal):
#     pass

# TODO: Implement DELETE endpoint to remove a criminal from the database
# @app.delete("/criminals/{criminal_id}")
# async def delete_criminal(criminal_id: int):
#     pass

# For running the application directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
