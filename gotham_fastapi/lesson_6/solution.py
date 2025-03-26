#!/usr/bin/env python3
"""
Justice League Database API - Complete Solution
----------------------------
A fully implemented API for the Justice League's meta-human database
using FastAPI with path and query parameters.
"""
from fastapi import FastAPI, Path, Query, HTTPException
from enum import Enum
from typing import List, Optional, Dict, Any
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

# Enum for sorting fields
class SortField(str, Enum):
    NAME = "name"
    POWER = "power_level"
    CITY = "base_city"

# Enum for sort direction
class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"

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
            "/heroes/power/{power_name}",
            "/heroes/{hero_id}/allies",
            "/stats",
            "/heroes/fulltext"
        ]
    }

@app.get("/heroes/")
async def list_heroes(
    active: Optional[bool] = None,
    min_power: Optional[int] = Query(None, ge=1, le=10, title="Minimum power level"),
    max_power: Optional[int] = Query(None, ge=1, le=10, title="Maximum power level"),
    sort_by: Optional[SortField] = Query(None, title="Field to sort by"),
    sort_dir: SortDirection = Query(SortDirection.ASC, title="Sort direction"),
    limit: int = Query(100, ge=1, le=100, title="Maximum number of heroes to return"),
    offset: int = Query(0, ge=0, title="Number of heroes to skip")
):
    """
    List all heroes with optional filtering and sorting.
    
    - **active**: Filter heroes by active status
    - **min_power**: Filter heroes with power level >= this value
    - **max_power**: Filter heroes with power level <= this value
    - **sort_by**: Field to sort results by
    - **sort_dir**: Sort direction (asc or desc)
    - **limit**: Maximum number of results to return
    - **offset**: Number of results to skip (for pagination)
    """
    results = heroes_db.copy()
    
    # Apply filters
    if active is not None:
        results = [h for h in results if h["active"] == active]
    
    if min_power is not None:
        results = [h for h in results if h["power_level"] >= min_power]
    
    if max_power is not None:
        results = [h for h in results if h["power_level"] <= max_power]
    
    # Apply sorting
    if sort_by:
        reverse = sort_dir == SortDirection.DESC
        results.sort(key=lambda x: x[sort_by], reverse=reverse)
    
    # Get total count before pagination
    total_count = len(results)
    
    # Apply pagination
    results = results[offset:offset + limit]
    
    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "heroes": results
    }

@app.get("/heroes/{hero_id}")
async def get_hero(
    hero_id: int = Path(
        ..., 
        title="The ID of the hero to retrieve",
        description="Must be a positive integer",
        ge=1,
        example=1
    )
):
    """
    Get detailed information about a specific hero by ID.
    
    - **hero_id**: The unique identifier of the hero
    """
    for hero in heroes_db:
        if hero["id"] == hero_id:
            return hero
    
    raise HTTPException(status_code=404, detail=f"Hero with ID {hero_id} not found")

@app.get("/heroes/type/{hero_type}")
async def get_heroes_by_type(
    hero_type: HeroType = Path(..., title="The type of heroes to retrieve")
):
    """
    Get heroes filtered by their type.
    
    - **hero_type**: Type of heroes to retrieve (super, vigilante, tech, magic)
    """
    results = [hero for hero in heroes_db if hero["hero_type"] == hero_type]
    
    if not results:
        raise HTTPException(
            status_code=404, 
            detail=f"No heroes found with type: {hero_type}"
        )
    
    return results

@app.get("/heroes/search")
async def search_heroes(
    name: Optional[str] = Query(None, min_length=2, title="Hero name to search for"),
    city: Optional[str] = Query(None, min_length=2, title="City to search for"),
    power: Optional[str] = Query(None, min_length=2, title="Power to search for"),
    min_level: Optional[int] = Query(None, ge=1, le=10, title="Minimum power level"),
    max_level: Optional[int] = Query(None, ge=1, le=10, title="Maximum power level"),
    active: Optional[bool] = Query(None, title="Filter by active status"),
    sort_by: Optional[SortField] = Query(None, title="Field to sort by"),
    sort_dir: SortDirection = Query(SortDirection.ASC, title="Sort direction"),
    limit: int = Query(10, ge=1, le=100, title="Maximum number of results"),
    offset: int = Query(0, ge=0, title="Number of results to skip")
):
    """
    Advanced search for heroes with multiple criteria.
    
    - **name**: Search for heroes whose names contain this string
    - **city**: Search for heroes based in cities containing this string
    - **power**: Search for heroes with powers containing this string
    - **min_level**: Filter heroes with power level >= this value
    - **max_level**: Filter heroes with power level <= this value
    - **active**: Filter heroes by active status
    - **sort_by**: Field to sort results by
    - **sort_dir**: Sort direction (asc or desc)
    - **limit**: Maximum number of results to return
    - **offset**: Number of results to skip (for pagination)
    """
    results = heroes_db.copy()
    
    # Apply filters based on provided parameters
    if name:
        results = [h for h in results if name.lower() in h["name"].lower()]
    
    if city:
        results = [h for h in results if city.lower() in h["base_city"].lower()]
    
    if power:
        results = [h for h in results if any(power.lower() in p.lower() for p in h["powers"])]
    
    if min_level is not None:
        results = [h for h in results if h["power_level"] >= min_level]
    
    if max_level is not None:
        results = [h for h in results if h["power_level"] <= max_level]
    
    if active is not None:
        results = [h for h in results if h["active"] == active]
    
    # Apply sorting
    if sort_by:
        reverse = sort_dir == SortDirection.DESC
        results.sort(key=lambda x: x[sort_by], reverse=reverse)
    
    # Get total count before pagination
    total_count = len(results)
    
    # Apply pagination
    results = results[offset:offset + limit]
    
    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "heroes": results
    }

@app.get("/heroes/power/{power_name}")
async def heroes_with_power(
    power_name: str = Path(..., min_length=2, title="Power to search for"),
    active: Optional[bool] = Query(None, title="Filter by active status")
):
    """
    Find heroes that have a specific power.
    
    - **power_name**: The power to search for
    - **active**: Optionally filter by active status
    """
    # Search case-insensitive
    power_name = power_name.lower()
    
    # Find heroes with this power
    results = [
        hero for hero in heroes_db 
        if any(power_name in p.lower() for p in hero["powers"])
    ]
    
    # Apply active filter if provided
    if active is not None:
        results = [h for h in results if h["active"] == active]
    
    if not results:
        raise HTTPException(
            status_code=404, 
            detail=f"No heroes found with power: {power_name}"
        )
    
    return results

@app.get("/heroes/{hero_id}/allies")
async def get_hero_allies(
    hero_id: int = Path(..., ge=1, title="Hero ID"),
    include_inactive: bool = Query(True, title="Include inactive allies"),
    details: bool = Query(True, title="Include full details of allies")
):
    """
    Get the allies of a specific hero.
    
    - **hero_id**: The ID of the hero
    - **include_inactive**: Whether to include inactive allies (default: yes)
    - **details**: Whether to include full details of allies (default: yes)
    """
    # Find the hero
    hero = None
    for h in heroes_db:
        if h["id"] == hero_id:
            hero = h
            break
    
    if hero is None:
        raise HTTPException(status_code=404, detail=f"Hero with ID {hero_id} not found")
    
    # Get allies
    ally_ids = hero.get("allies", [])
    allies = []
    
    for ally_id in ally_ids:
        for h in heroes_db:
            if h["id"] == ally_id:
                # Check if we should include inactive allies
                if include_inactive or h["active"]:
                    if details:
                        allies.append(h)
                    else:
                        allies.append({"id": h["id"], "name": h["name"]})
                break
    
    return {
        "hero": hero["name"],
        "ally_count": len(allies),
        "allies": allies
    }

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

# Knightfall Protocol Enhancement - Fulltext Search
@app.get("/heroes/fulltext")
async def fulltext_search(
    q: str = Query(..., min_length=2, title="Search query"),
    limit: int = Query(10, ge=1, le=100, title="Maximum number of results"),
    offset: int = Query(0, ge=0, title="Number of results to skip")
):
    """
    Full-text search across hero records.
    Searches in name, real_name, city, and powers.
    Results are sorted by relevance.
    
    - **q**: Search query (minimum 2 characters)
    - **limit**: Maximum number of results to return
    - **offset**: Number of results to skip (for pagination)
    """
    q = q.lower()
    results = []
    
    for hero in heroes_db:
        # Calculate a relevance score based on where the query appears
        relevance = 0
        
        # Check name (highest relevance)
        if q in hero["name"].lower():
            relevance += 5
        
        # Check real name (high relevance)
        if q in hero["real_name"].lower():
            relevance += 3
        
        # Check city (medium relevance)
        if q in hero["base_city"].lower():
            relevance += 2
        
        # Check powers (lower but cumulative relevance)
        power_matches = sum(1 for power in hero["powers"] if q in power.lower())
        relevance += power_matches
        
        # Check weakness (lower relevance)
        weakness_matches = sum(1 for weakness in hero["weaknesses"] if q in weakness.lower()) 
        relevance += weakness_matches
        
        # If there's any relevance, add to results
        if relevance > 0:
            hero_copy = hero.copy()
            hero_copy["relevance"] = relevance
            results.append(hero_copy)
    
    # Sort by relevance
    results.sort(key=lambda x: x["relevance"], reverse=True)
    
    # Get total before pagination
    total = len(results)
    
    # Apply pagination
    results = results[offset:offset + limit]
    
    return {
        "total": total,
        "query": q,
        "limit": limit,
        "offset": offset,
        "heroes": results
    }

# Knightfall Protocol Enhancement - Heroes by common power
@app.get("/heroes/{hero_id}/similar")
async def find_similar_heroes(
    hero_id: int = Path(..., ge=1, title="Hero ID"),
    min_common_powers: int = Query(1, ge=1, title="Minimum common powers"),
    limit: int = Query(5, ge=1, le=20, title="Maximum number of similar heroes")
):
    """
    Find heroes with similar powers to the specified hero.
    
    - **hero_id**: The ID of the hero to find similar heroes for
    - **min_common_powers**: Minimum number of powers that must overlap
    - **limit**: Maximum number of similar heroes to return
    """
    # Find the hero
    hero = None
    for h in heroes_db:
        if h["id"] == hero_id:
            hero = h
            break
    
    if hero is None:
        raise HTTPException(status_code=404, detail=f"Hero with ID {hero_id} not found")
    
    # Get the hero's powers
    hero_powers = set(p.lower() for p in hero["powers"])
    
    # Find similar heroes
    similar_heroes = []
    
    for h in heroes_db:
        if h["id"] == hero_id:
            continue  # Skip the hero we're comparing to
        
        other_powers = set(p.lower() for p in h["powers"])
        common_powers = hero_powers.intersection(other_powers)
        
        if len(common_powers) >= min_common_powers:
            hero_copy = h.copy()
            hero_copy["common_powers"] = list(common_powers)
            hero_copy["common_power_count"] = len(common_powers)
            similar_heroes.append(hero_copy)
    
    # Sort by number of common powers
    similar_heroes.sort(key=lambda x: x["common_power_count"], reverse=True)
    
    # Limit results
    similar_heroes = similar_heroes[:limit]
    
    return {
        "hero": hero["name"],
        "similar_heroes": similar_heroes
    }

# For running the application directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
