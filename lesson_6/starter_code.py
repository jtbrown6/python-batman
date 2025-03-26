#!/usr/bin/env python3
"""
Justice League Database API
----------------------------
Your mission: Create a comprehensive API for the Justice League's meta-human database
using FastAPI with path and query parameters.
"""
from fastapi import FastAPI, Path, Query, HTTPException
from enum import Enum
from typing import List, Optional
import uvicorn

# Initialize our Justice League API
app = FastAPI(
    title="Justice League Database",
    description="Access to the Justice League's meta-human and hero records",
    version="1.0.0"
)

# Sample database of heroes (in a real app, this would be a database)
heroes_db = [
    {
        "id": 1,
        "name": "Batman",
        "real_name": "Bruce Wayne",
        "hero_type": "vigilante",
        "base_city": "Gotham",
        "active": True,
        "power_level": 7,
        "powers": ["Intelligence", "Martial Arts", "Technology", "Wealth"],
        "weaknesses": ["No Superpowers", "Human Limitations"],
        "allies": [3, 5, 6]
    },
    {
        "id": 2,
        "name": "Superman",
        "real_name": "Clark Kent",
        "hero_type": "super",
        "base_city": "Metropolis",
        "active": True,
        "power_level": 10,
        "powers": ["Flight", "Super Strength", "Heat Vision", "X-Ray Vision", "Invulnerability"],
        "weaknesses": ["Kryptonite", "Magic"],
        "allies": [4, 7]
    },
    {
        "id": 3,
        "name": "Nightwing",
        "real_name": "Dick Grayson",
        "hero_type": "vigilante",
        "base_city": "Blüdhaven",
        "active": True,
        "power_level": 6,
        "powers": ["Acrobatics", "Martial Arts", "Detective Skills"],
        "weaknesses": ["No Superpowers", "Human Limitations"],
        "allies": [1, 6]
    },
    {
        "id": 4,
        "name": "Wonder Woman",
        "real_name": "Diana Prince",
        "hero_type": "super",
        "base_city": "Themyscira",
        "active": True,
        "power_level": 9,
        "powers": ["Super Strength", "Flight", "Combat Skill", "Lasso of Truth"],
        "weaknesses": ["Binding by a Man (Historical)"],
        "allies": [2, 7]
    },
    {
        "id": 5,
        "name": "Red Hood",
        "real_name": "Jason Todd",
        "hero_type": "vigilante",
        "base_city": "Gotham",
        "active": True,
        "power_level": 5,
        "powers": ["Marksmanship", "Combat Training", "Tactical Skills"],
        "weaknesses": ["Emotional Instability", "Human Limitations"],
        "allies": [1]
    },
    {
        "id": 6,
        "name": "Batgirl",
        "real_name": "Barbara Gordon",
        "hero_type": "vigilante",
        "base_city": "Gotham",
        "active": True,
        "power_level": 6,
        "powers": ["Intelligence", "Hacking", "Martial Arts"],
        "weaknesses": ["Human Limitations"],
        "allies": [1, 3]
    },
    {
        "id": 7,
        "name": "The Flash",
        "real_name": "Barry Allen",
        "hero_type": "super",
        "base_city": "Central City",
        "active": True,
        "power_level": 8,
        "powers": ["Super Speed", "Speed Force Connection", "Phasing"],
        "weaknesses": ["Must Eat Frequently", "Can Trip"],
        "allies": [2, 4]
    },
    {
        "id": 8,
        "name": "Green Arrow",
        "real_name": "Oliver Queen",
        "hero_type": "vigilante",
        "base_city": "Star City",
        "active": False,
        "power_level": 5,
        "powers": ["Archery", "Combat Skills", "Tactical Mind"],
        "weaknesses": ["Human Limitations", "Limited Range"],
        "allies": []
    }
]

# Enum for hero types
class HeroType(str, Enum):
    SUPER = "super"
    VIGILANTE = "vigilante"
    TECH = "tech"
    MAGIC = "magic"

# Root endpoint
@app.get("/")
async def justice_league_welcome():
    """Welcome message for the Justice League Database API."""
    return {
        "message": "Welcome to the Justice League Database. Authorization required for full access.",
        "available_endpoints": [
            "/heroes",
            "/heroes/{hero_id}",
            "/heroes/type/{hero_type}",
            "/heroes/search",
            "/stats"
        ]
    }

# TODO: Implement endpoint to list all heroes with optional filtering
# @app.get("/heroes/")
# async def list_heroes(...):
#     """List all heroes with optional filtering."""
#     pass

# TODO: Implement endpoint to get a specific hero by ID with path validation
# @app.get("/heroes/{hero_id}")
# async def get_hero(hero_id: ...):
#     """Get a hero by their ID."""
#     pass

# TODO: Implement endpoint to get heroes by their type using Enum path parameter
# @app.get("/heroes/type/{hero_type}")
# async def get_heroes_by_type(hero_type: ...):
#     """Get heroes by their type (super, vigilante, tech, magic)."""
#     pass

# TODO: Implement advanced search endpoint with multiple query parameters
# @app.get("/heroes/search")
# async def search_heroes(...):
#     """
#     Advanced search for heroes with multiple criteria.
#     """
#     pass

# TODO: Implement an endpoint to get heroes with a specific power
# @app.get("/heroes/power/{power_name}")
# async def heroes_with_power(...):
#     """Find heroes that have a specific power."""
#     pass

# TODO: Implement an endpoint to get a hero's allies with path and query parameters
# @app.get("/heroes/{hero_id}/allies")
# async def get_hero_allies(...):
#     """Get the allies of a specific hero."""
#     pass

# Stats endpoint - already implemented as an example
@app.get("/stats")
async def get_statistics():
    """Get overall statistics about heroes in the database."""
    active_count = sum(1 for hero in heroes_db if hero["active"])
    inactive_count = len(heroes_db) - active_count
    
    # Count heroes by type
    hero_types = {}
    for hero in heroes_db:
        hero_type = hero["hero_type"]
        hero_types[hero_type] = hero_types.get(hero_type, 0) + 1
    
    # Get average power level
    avg_power = sum(hero["power_level"] for hero in heroes_db) / len(heroes_db)
    
    # Most common powers
    power_count = {}
    for hero in heroes_db:
        for power in hero["powers"]:
            power_count[power] = power_count.get(power, 0) + 1
    
    top_powers = sorted(power_count.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "total_heroes": len(heroes_db),
        "active_heroes": active_count,
        "inactive_heroes": inactive_count,
        "heroes_by_type": hero_types,
        "average_power_level": round(avg_power, 1),
        "top_powers": dict(top_powers)
    }

# For running the application directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
