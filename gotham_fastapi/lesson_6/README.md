# Lesson 6: Power Classification System (Path & Query Parameters)

## Justice League Database

Just as Batman maintains detailed files on meta-humans and their abilities, FastAPI allows us to efficiently filter, search, and organize resources through path and query parameters. These are crucial for creating flexible, user-friendly APIs.

## Why Parameters Matter in API Design

Parameters give your API users the power to:

1. **Request exactly what they need** - Like Batman pulling up just Joker's file rather than all criminals
2. **Filter large datasets** - Such as finding all meta-humans with super-strength
3. **Control response format** - Just as Batman can view data as text or holographic display
4. **Enable flexible search options** - Find heroes active in a particular city or with specific abilities

Well-designed parameters make your API both powerful and intuitive to use. Think of it as organizing the Batcomputer's vast database for optimal access.

## Types of Parameters in FastAPI

FastAPI supports several types of parameters, each with different purposes:

### 1. Path Parameters: The Direct Route

Path parameters are part of the URL path itself and are typically used to identify a specific resource:

```
/heroes/{hero_id}
/villains/{villain_id}/powers
/cities/{city_name}/incidents
```

They are:
- **Required** - The endpoint won't match without them
- **Position-based** - Their position in the URL path matters
- **Resource-focused** - Usually identify a specific resource

### 2. Query Parameters: The Search Criteria

Query parameters appear after the `?` in a URL and are used for filtering, sorting, and pagination:

```
/heroes?name=flash&city=central
/incidents?date_from=2023-01-01&status=active
/powers?type=energy&strength=high
```

They are:
- **Optional** (typically) - The endpoint works without them
- **Named** - Their order doesn't matter
- **Filter-focused** - Usually modify or filter results

### 3. Request Body Parameters (covered in Lesson 7)

Used for complex data that's too large for URLs, like creating or updating resources.

## Learning Objectives
- Master path parameters for resource identification
- Implement query parameters for filtering and searching
- Define parameter types and validation
- Create Enum-based parameters
- Combine multiple parameter types in a single endpoint

## Path Parameters in Detail

### Basic Path Parameters

Path parameters are defined in the route path with curly braces `{}`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/heroes/{hero_id}")
async def get_hero(hero_id: int):
    """Get a hero by their ID."""
    heroes = {
        1: {"id": 1, "name": "Batman", "city": "Gotham", "powers": ["Intelligence", "Wealth"]},
        2: {"id": 2, "name": "Superman", "city": "Metropolis", "powers": ["Flight", "Strength"]}
    }
    
    if hero_id not in heroes:
        return {"error": "Hero not found"}
    
    return heroes[hero_id]
```

Key points:
- `{hero_id}` in the path indicates a path parameter
- `hero_id: int` in the function performs automatic conversion and validation
- FastAPI will return a validation error if a non-integer is provided

### Path Parameters with Validation

You can add validation to path parameters using Pydantic's `Field` or FastAPI's `Path`:

```python
from fastapi import FastAPI, Path

@app.get("/heroes/{hero_id}")
async def get_hero(
    hero_id: int = Path(..., title="The ID of the hero", ge=1)
):
    """Get a hero by their ID (must be positive)."""
    # Implementation...
```

The `...` is Python's ellipsis syntax, indicating the parameter is required. The `ge=1` parameter enforces that `hero_id` must be greater than or equal to 1.

### Path Parameters with Enum Values

For parameters with a fixed set of valid values, use Python's Enum:

```python
from enum import Enum
from fastapi import FastAPI

class HeroType(str, Enum):
    SUPER = "super"
    VIGILANTE = "vigilante"
    TECH = "tech"
    MAGIC = "magic"

app = FastAPI()

@app.get("/heroes/type/{hero_type}")
async def get_heroes_by_type(hero_type: HeroType):
    """Get heroes by their type."""
    return {"hero_type": hero_type, "message": f"Getting all {hero_type.value} heroes"}
```

With enums:
- FastAPI validates that the parameter value matches one of the enum values
- Your API documentation automatically shows the allowed values
- Python gives you type checking for these parameters

## Query Parameters in Detail

### Basic Query Parameters

Query parameters don't need to be declared in the path. They're automatically picked up from the function parameters:

```python
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/heroes/")
async def list_heroes(
    name: Optional[str] = None,
    city: Optional[str] = None,
    active: bool = True
):
    """List heroes with optional filtering."""
    heroes = [
        {"id": 1, "name": "Batman", "city": "Gotham", "active": True},
        {"id": 2, "name": "Superman", "city": "Metropolis", "active": True},
        {"id": 3, "name": "Nightwing", "city": "Blüdhaven", "active": True},
        {"id": 4, "name": "Green Arrow", "city": "Star City", "active": False}
    ]
    
    results = heroes.copy()
    
    # Apply filters based on provided parameters
    if name:
        results = [h for h in results if name.lower() in h["name"].lower()]
    
    if city:
        results = [h for h in results if city.lower() in h["city"].lower()]
    
    if active is not None:
        results = [h for h in results if h["active"] == active]
    
    return results
```

Key points:
- Default values make parameters optional
- Type annotations provide validation
- The function's logic uses parameters to filter results

### Query Parameters with Validation

Just like path parameters, you can validate query parameters:

```python
from fastapi import FastAPI, Query
from typing import Optional

@app.get("/incidents/")
async def list_incidents(
    city: str = Query(..., min_length=2, max_length=50),
    severity: Optional[int] = Query(None, ge=1, le=10),
    limit: int = Query(20, ge=1, le=100)
):
    """List incidents with validation."""
    # Implementation...
```

Here we're:
- Making `city` a required parameter with length validation
- Making `severity` optional but validating its range if provided
- Setting a default for `limit` with a valid range (pagination)

### Multiple Values for a Query Parameter

Sometimes you want to allow multiple values for the same parameter:

```python
from fastapi import FastAPI
from typing import List

app = FastAPI()

@app.get("/heroes/")
async def list_heroes(
    powers: List[str] = Query(None)
):
    """Get heroes that have all the specified powers."""
    # This will handle requests like /heroes/?powers=flight&powers=strength
    
    return {"powers_required": powers, "message": "Getting heroes with all specified powers"}
```

In the URL, this would look like: `/heroes/?powers=flight&powers=strength`

### Query Parameters for Advanced Filtering

By combining query parameters, you can create powerful search endpoints:

```python
from fastapi import FastAPI, Query
from typing import Optional, List
from enum import Enum

class PowerType(str, Enum):
    PHYSICAL = "physical"
    MENTAL = "mental"
    ENERGY = "energy"
    TECH = "tech"
    MAGIC = "magic"

app = FastAPI()

@app.get("/powers/")
async def search_powers(
    name: Optional[str] = None,
    type: Optional[PowerType] = None,
    strength_min: Optional[int] = Query(None, ge=1, le=10),
    strength_max: Optional[int] = Query(None, ge=1, le=10),
    heroes_with_power: Optional[List[str]] = Query(None)
):
    """Advanced power search with multiple filtering options."""
    # Implementation...
```

## Combining Path and Query Parameters

You can use both types of parameters in a single endpoint:

```python
from fastapi import FastAPI, Path, Query
from typing import Optional

app = FastAPI()

@app.get("/cities/{city_name}/incidents")
async def get_city_incidents(
    city_name: str = Path(..., min_length=2),
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    type: Optional[str] = None,
    severity: Optional[int] = Query(None, ge=1, le=10),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get incidents for a specific city with filtering and pagination."""
    # Implementation...
```

This approach gives you the best of both worlds:
- Path parameter for the primary resource (city)
- Query parameters for filtering, sorting, and pagination

## Path Parameter Precedence

When defining your endpoints, be aware of path overlaps. FastAPI evaluates routes in order:

```python
@app.get("/heroes/{hero_id}")
async def get_hero(hero_id: int):
    # This will match /heroes/123
    return {"hero_id": hero_id}

@app.get("/heroes/stats")
async def get_hero_stats():
    # This will NEVER be reached if defined after the previous route
    # because /heroes/stats would match the {hero_id} pattern
    return {"stats": "Heroes statistics"}
```

To fix this, define more specific routes first:

```python
@app.get("/heroes/stats")
async def get_hero_stats():
    # Now this will match correctly
    return {"stats": "Heroes statistics"}

@app.get("/heroes/{hero_id}")
async def get_hero(hero_id: int):
    # This will match everything else
    return {"hero_id": hero_id}
```

## Project: Justice League Database API

Your mission is to create a comprehensive API for the Justice League's meta-human database. The system should:

1. Define endpoints for browsing heroes by various criteria
2. Implement path parameters for accessing specific hero details
3. Create endpoints with advanced query parameters for searching heroes by powers, location, status, etc.
4. Add validation to ensure data quality

Create a file named `justice_league_api.py` using the starter code provided.

## The Knightfall Protocol (Push Harder Challenge)

Enhance your Justice League Database API to:
1. Implement pagination for all list endpoints
2. Add sorting options (by name, power level, etc.)
3. Create relationship endpoints (e.g., heroes with similar powers, known allies)
4. Implement a full-text search feature across multiple fields
5. Add response models for consistent API output

## Resources

- Check out `starter_code.py` to get started
- If you need guidance, look at the `helper_guide.md` file for "Bruce Wayne's Journal"
- After you've tried solving it yourself, you can check `solution.py` for one possible implementation

Remember, in the words of Batman: "It's not just who you are underneath, but what you can provide through your API endpoints that defines you."
