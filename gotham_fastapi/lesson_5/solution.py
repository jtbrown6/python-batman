#!/usr/bin/env python3
"""
Batcomputer Criminal Database API - Complete Solution
----------------------------
A fully implemented RESTful API for Batman's criminal database
using FastAPI, including Knightfall Protocol enhancements.
"""
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

# Define Pydantic models
class Crime(BaseModel):
    """Model for a crime committed by a criminal."""
    name: str
    description: Optional[str] = None
    date: str
    location: str
    evidence: List[str] = []

class CriminalBase(BaseModel):
    """Base model for criminal data."""
    name: str
    status: str
    threat_level: str = "Unknown"
    last_known_location: Optional[str] = None
    psycho_profile: Optional[str] = None

class CriminalCreate(CriminalBase):
    """Model used for creating a new criminal."""
    known_associates: List[str] = []

class CriminalWithCrimes(CriminalBase):
    """Enhanced model that includes crimes and associates."""
    id: int
    crimes: List[Crime] = []
    known_associates: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Joker",
                "status": "At large",
                "threat_level": "Extreme",
                "last_known_location": "Amusement Mile",
                "psycho_profile": "Psychopath with a theatrical flair",
                "known_associates": ["Harley Quinn", "Riddler"],
                "crimes": [
                    {
                        "name": "Bank Robbery",
                        "description": "Stole $1M and left joker cards",
                        "date": "2025-03-01",
                        "location": "Gotham National Bank",
                        "evidence": ["Joker cards", "CCTV footage"]
                    }
                ]
            }
        }

class CriminalResponse(CriminalBase):
    """Model for returning a criminal with ID."""
    id: int
    known_associates: List[str] = []

# Initialize the Batcomputer API
app = FastAPI(
    title="Batcomputer API",
    description="Access to Batman's criminal database and Gotham City information",
    version="1.0.0"
)

# Sample criminal database
criminals_db = [
    {
        "id": 1, 
        "name": "Joker", 
        "status": "At large", 
        "threat_level": "Extreme", 
        "last_known_location": "Amusement Mile", 
        "psycho_profile": "Psychopath with a theatrical flair",
        "known_associates": ["Harley Quinn"],
        "crimes": [
            {
                "name": "Bank Robbery",
                "description": "Stole $1M and left joker cards",
                "date": "2025-03-01",
                "location": "Gotham National Bank",
                "evidence": ["Joker cards", "CCTV footage"]
            },
            {
                "name": "Arkham Breakout",
                "description": "Orchestrated mass escape from Arkham Asylum",
                "date": "2025-02-15",
                "location": "Arkham Asylum",
                "evidence": ["Security footage", "Guard testimony"]
            }
        ]
    },
    {
        "id": 2, 
        "name": "Penguin", 
        "status": "In custody", 
        "threat_level": "High", 
        "last_known_location": "Blackgate Prison", 
        "psycho_profile": "Narcissistic with inferiority complex",
        "known_associates": ["Riddler", "Catwoman"],
        "crimes": [
            {
                "name": "Weapons Smuggling",
                "description": "Smuggled military-grade weapons into Gotham",
                "date": "2025-01-20",
                "location": "Gotham Harbor",
                "evidence": ["Weapons cache", "Financial records"]
            }
        ]
    },
    {
        "id": 3, 
        "name": "Riddler", 
        "status": "Unknown", 
        "threat_level": "High", 
        "last_known_location": "Cyberspace", 
        "psycho_profile": "Obsessive-compulsive with superiority complex",
        "known_associates": ["Penguin"],
        "crimes": [
            {
                "name": "City Infrastructure Hack",
                "description": "Took control of traffic lights and electronic billboards",
                "date": "2025-02-28",
                "location": "Gotham City",
                "evidence": ["Digital fingerprint", "Riddles left in code"]
            }
        ]
    },
    {
        "id": 4, 
        "name": "Harley Quinn", 
        "status": "At large", 
        "threat_level": "High", 
        "last_known_location": "Amusement Mile", 
        "psycho_profile": "Codependent personality with manic tendencies",
        "known_associates": ["Joker", "Poison Ivy"],
        "crimes": [
            {
                "name": "Jewelry Store Heist",
                "description": "Stole diamonds while causing extensive property damage",
                "date": "2025-03-05",
                "location": "Gotham Diamond Exchange",
                "evidence": ["Mallet marks", "Playing card confetti"]
            }
        ]
    },
    {
        "id": 5, 
        "name": "Poison Ivy", 
        "status": "At large", 
        "threat_level": "High", 
        "last_known_location": "Robinson Park", 
        "psycho_profile": "Eco-terrorist with misanthropic tendencies",
        "known_associates": ["Harley Quinn"],
        "crimes": [
            {
                "name": "Botanical Gardens Takeover",
                "description": "Converted botanical gardens into mutant plant fortress",
                "date": "2025-02-10",
                "location": "Gotham Botanical Gardens",
                "evidence": ["Mutated plant samples", "Toxin traces"]
            }
        ]
    }
]

# Root endpoint
@app.get("/")
async def batcomputer_welcome():
    """Welcome message for the Batcomputer API."""
    return {"message": "Welcome to the Batcomputer. Authorize to proceed."}

# CRUD Operations

@app.get("/criminals/", response_model=List[CriminalResponse])
async def list_criminals():
    """Get a list of all known criminals in the database."""
    return criminals_db

@app.get("/criminals/{criminal_id}", response_model=CriminalWithCrimes)
async def get_criminal(criminal_id: int):
    """Get detailed information about a specific criminal by ID."""
    for criminal in criminals_db:
        if criminal["id"] == criminal_id:
            return criminal
    raise HTTPException(status_code=404, detail="Criminal not found")

@app.get("/criminals/search")
async def search_criminals(
    name: Optional[str] = None,
    status: Optional[str] = None,
    threat_level: Optional[str] = None
):
    """Search for criminals by name, status, and/or threat level."""
    results = criminals_db.copy()
    
    if name:
        results = [c for c in results if name.lower() in c["name"].lower()]
    
    if status:
        results = [c for c in results if status.lower() in c["status"].lower()]
    
    if threat_level:
        results = [c for c in results if threat_level.lower() == c["threat_level"].lower()]
    
    return results

@app.post("/criminals/", status_code=status.HTTP_201_CREATED, response_model=CriminalResponse)
async def create_criminal(criminal: CriminalCreate):
    """Add a new criminal to the database."""
    # Generate new ID
    new_id = max(c["id"] for c in criminals_db) + 1
    
    # Create new criminal dict with ID
    new_criminal = criminal.dict()
    new_criminal["id"] = new_id
    new_criminal["crimes"] = []  # Initialize empty crimes list
    
    # Add to our "database"
    criminals_db.append(new_criminal)
    
    return new_criminal

@app.put("/criminals/{criminal_id}", response_model=CriminalResponse)
async def update_criminal(criminal_id: int, criminal: CriminalCreate):
    """Update an existing criminal's information."""
    for i, c in enumerate(criminals_db):
        if c["id"] == criminal_id:
            # Update the criminal but preserve ID and crimes
            updated_criminal = criminal.dict()
            updated_criminal["id"] = criminal_id
            updated_criminal["crimes"] = c.get("crimes", [])
            criminals_db[i] = updated_criminal
            return updated_criminal
    
    raise HTTPException(status_code=404, detail="Criminal not found")

@app.delete("/criminals/{criminal_id}")
async def delete_criminal(criminal_id: int):
    """Remove a criminal from the database."""
    for i, c in enumerate(criminals_db):
        if c["id"] == criminal_id:
            # Remove from the list
            deleted = criminals_db.pop(i)
            return {"message": f"Criminal {deleted['name']} deleted"}
    
    raise HTTPException(status_code=404, detail="Criminal not found")

# Knightfall Protocol Enhancements

@app.get("/criminals/threat-level/{level}")
async def criminals_by_threat_level(level: str):
    """Filter criminals by their threat level."""
    results = [c for c in criminals_db if c["threat_level"].lower() == level.lower()]
    if not results:
        raise HTTPException(status_code=404, detail=f"No criminals found with threat level: {level}")
    return results

@app.get("/criminals/advanced-search")
async def advanced_search(
    name: Optional[str] = None,
    status: Optional[str] = None,
    threat_level: Optional[str] = None,
    location: Optional[str] = None,
    associated_with: Optional[str] = None
):
    """
    Advanced search with multiple criteria.
    
    Use any combination of parameters to filter the results.
    """
    # Start with all criminals
    results = criminals_db.copy()
    
    # Apply each filter if provided
    if name:
        results = [c for c in results if name.lower() in c["name"].lower()]
    
    if status:
        results = [c for c in results if status.lower() in c["status"].lower()]
    
    if threat_level:
        results = [c for c in results if threat_level.lower() == c["threat_level"].lower()]
    
    if location:
        results = [c for c in results if location.lower() in c.get("last_known_location", "").lower()]
    
    if associated_with:
        results = [c for c in results if "known_associates" in c and 
                  any(associated_with.lower() in associate.lower() for associate in c["known_associates"])]
    
    return results

@app.get("/criminals/{criminal_id}/associates")
async def get_criminal_associates(criminal_id: int):
    """Get details about a criminal's known associates."""
    # Find the criminal
    criminal = None
    for c in criminals_db:
        if c["id"] == criminal_id:
            criminal = c
            break
    
    if not criminal:
        raise HTTPException(status_code=404, detail="Criminal not found")
    
    # Get their associates
    associates = criminal.get("known_associates", [])
    
    # Find full records of these associates
    associate_records = []
    for associate_name in associates:
        for c in criminals_db:
            if c["name"] == associate_name:
                associate_records.append(c)
                break
    
    return {
        "criminal": criminal["name"],
        "associates": associate_records
    }

@app.post("/criminals/{criminal_id}/crimes", status_code=status.HTTP_201_CREATED)
async def add_crime(criminal_id: int, crime: Crime):
    """Add a new crime to a criminal's record."""
    # Find the criminal
    criminal = None
    for i, c in enumerate(criminals_db):
        if c["id"] == criminal_id:
            criminal = c
            criminal_idx = i
            break
    
    if not criminal:
        raise HTTPException(status_code=404, detail="Criminal not found")
    
    # Add the crime to their record
    if "crimes" not in criminal:
        criminal["crimes"] = []
    
    criminal["crimes"].append(crime.dict())
    criminals_db[criminal_idx] = criminal
    
    return {
        "message": f"Crime added to {criminal['name']}'s record",
        "crime": crime
    }

@app.get("/criminals/{criminal_id}/crimes")
async def get_criminal_crimes(criminal_id: int):
    """Get a list of crimes committed by a specific criminal."""
    # Find the criminal
    for c in criminals_db:
        if c["id"] == criminal_id:
            return {
                "criminal": c["name"],
                "crimes": c.get("crimes", [])
            }
    
    raise HTTPException(status_code=404, detail="Criminal not found")

@app.get("/locations")
async def list_criminal_locations():
    """Get a list of all locations where criminals have been spotted."""
    locations = set()
    
    # Collect all known locations from criminals
    for criminal in criminals_db:
        if criminal.get("last_known_location"):
            locations.add(criminal["last_known_location"])
    
    # Also collect all crime locations
    for criminal in criminals_db:
        for crime in criminal.get("crimes", []):
            if crime.get("location"):
                locations.add(crime["location"])
    
    return {"locations": sorted(list(locations))}

@app.get("/status-report")
async def status_report():
    """Generate a summary status report for Batman."""
    total_criminals = len(criminals_db)
    at_large = sum(1 for c in criminals_db if c.get("status", "").lower() == "at large")
    in_custody = sum(1 for c in criminals_db if c.get("status", "").lower() == "in custody")
    unknown = total_criminals - at_large - in_custody
    
    high_threat = sum(1 for c in criminals_db if c.get("threat_level", "").lower() in ["high", "extreme"])
    
    total_crimes = sum(len(c.get("crimes", [])) for c in criminals_db)
    
    recent_criminal_activity = [
        {
            "criminal": c["name"],
            "status": c["status"],
            "threat_level": c["threat_level"],
            "location": c["last_known_location"],
            "recent_crime": c["crimes"][-1]["name"] if c.get("crimes") else "None"
        }
        for c in criminals_db
        if c.get("status", "").lower() == "at large" and c.get("crimes")
    ]
    
    return {
        "total_criminals_tracked": total_criminals,
        "criminals_at_large": at_large,
        "criminals_in_custody": in_custody,
        "criminals_status_unknown": unknown,
        "high_threat_criminals": high_threat,
        "total_documented_crimes": total_crimes,
        "recent_criminal_activity": recent_criminal_activity
    }

# For running the application directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
