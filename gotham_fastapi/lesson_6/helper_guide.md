# Bruce Wayne's Journal: Justice League Database API

## Thought Process for Path and Query Parameters

When I designed the Justice League Database API, I focused on creating intuitive, flexible, and efficient access paths to our hero records. Much like organizing the Batcave's equipment, a well-designed API makes information retrieval swift and precise.

### 1. Planning the API Structure

**Thought process:**
- Need clear, logical URL paths that reflect resource hierarchy
- Need to balance between specific endpoints and flexibility
- Must consider security implications of exposing certain data
- Want to enable powerful search capabilities without complexity

**Solution approach:**
- Create a RESTful API structure with clear resource naming
- Use path parameters for specific resource identification
- Use query parameters for filtering and modifying results
- Implement validation to protect against bad inputs

### 2. Implementing Basic Hero Listing with Filtering

**Thought process:**
- Users may want to see all heroes or filter by certain criteria
- Some filters are common enough to warrant dedicated parameters
- Need to handle optional parameters gracefully
- Want to keep the implementation simple but powerful

**Pseudo-code:**
```
Function list_heroes(active: Optional[bool], min_power: Optional[int], max_power: Optional[int]):
    Start with all heroes in database
    If active parameter is provided:
        Filter heroes by active status
    If min_power parameter is provided:
        Filter heroes with power_level >= min_power
    If max_power parameter is provided:
        Filter heroes with power_level <= max_power
    Return filtered heroes
```

**Implementation hints:**
```python
@app.get("/heroes/")
async def list_heroes(
    active: Optional[bool] = None,
    min_power: Optional[int] = Query(None, ge=1, le=10),
    max_power: Optional[int] = Query(None, ge=1, le=10)
):
    """List all heroes with optional filtering."""
    results = heroes_db.copy()
    
    if active is not None:
        results = [h for h in results if h["active"] == active]
    
    if min_power is not None:
        results = [h for h in results if h["power_level"] >= min_power]
    
    if max_power is not None:
        results = [h for h in results if h["power_level"] <= max_power]
    
    return results
```

### 3. Finding a Specific Hero by ID

**Thought process:**
- Need to validate that IDs are valid integers
- Need to handle the case where a hero doesn't exist
- Should provide clear error messages
- Path parameters are ideal for resource identification

**Pseudo-code:**
```
Function get_hero(hero_id: int):
    Validate that hero_id is positive
    Search for hero with matching ID
    If found, return the hero data
    If not found, return a 404 error with clear message
```

**Implementation hints:**
```python
@app.get("/heroes/{hero_id}")
async def get_hero(
    hero_id: int = Path(..., title="The ID of the hero to get", ge=1)
):
    """Get a hero by their ID."""
    for hero in heroes_db:
        if hero["id"] == hero_id:
            return hero
    
    raise HTTPException(status_code=404, detail=f"Hero with ID {hero_id} not found")
```

### 4. Filtering Heroes by Type Using Enums

**Thought process:**
- There are only certain valid hero types
- An enum provides validation and documentation
- Path parameter makes semantic sense for this filter
- Need to handle the case where no heroes match

**Pseudo-code:**
```
Function get_heroes_by_type(hero_type: HeroType):
    Filter heroes to only those matching the specified type
    If no heroes found, return an empty list (or could return 404)
    Return the filtered heroes
```

**Implementation hints:**
```python
@app.get("/heroes/type/{hero_type}")
async def get_heroes_by_type(
    hero_type: HeroType
):
    """Get heroes by their type (super, vigilante, tech, magic)."""
    results = [hero for hero in heroes_db if hero["hero_type"] == hero_type]
    return results
```

### 5. Advanced Search with Multiple Parameters

**Thought process:**
- Need a flexible endpoint for complex searches
- Multiple optional parameters allow combining filters
- String searches should be case-insensitive and partial matches
- Should provide pagination for large result sets

**Pseudo-code:**
```
Function search_heroes(name, city, power, min_level, max_level, limit, offset):
    Start with all heroes
    Apply each filter if the parameter was provided
    Apply pagination using limit and offset
    Return the paginated, filtered results
```

**Implementation hints:**
```python
@app.get("/heroes/search")
async def search_heroes(
    name: Optional[str] = None,
    city: Optional[str] = None,
    power: Optional[str] = None,
    min_level: Optional[int] = Query(None, ge=1, le=10),
    max_level: Optional[int] = Query(None, ge=1, le=10),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Advanced search for heroes with multiple criteria.
    Also supports pagination with limit and offset.
    """
    results = heroes_db.copy()
    
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
    
    # Apply pagination
    total = len(results)
    results = results[offset:offset + limit]
    
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "heroes": results
    }
```

### 6. Finding Heroes with a Specific Power

**Thought process:**
- Path parameter for the power name makes semantic sense
- Need to handle case sensitivity and partial matches
- Should validate the power name in some way

**Pseudo-code:**
```
Function heroes_with_power(power_name: str):
    Find all heroes whose powers list contains the specified power
    Return the matching heroes or a message if none found
```

**Implementation hints:**
```python
@app.get("/heroes/power/{power_name}")
async def heroes_with_power(
    power_name: str = Path(..., min_length=2)
):
    """Find heroes that have a specific power."""
    # Search case-insensitive
    power_name = power_name.lower()
    
    # Find heroes with this power
    results = [
        hero for hero in heroes_db 
        if any(power_name in p.lower() for p in hero["powers"])
    ]
    
    if not results:
        raise HTTPException(status_code=404, detail=f"No heroes found with power: {power_name}")
    
    return results
```

### 7. Getting a Hero's Allies

**Thought process:**
- Combines path parameter (hero ID) with potential query parameters
- Need to handle case where hero doesn't exist
- Need to convert ally IDs to full hero objects
- Could add filtering on the allies themselves

**Pseudo-code:**
```
Function get_hero_allies(hero_id: int, include_inactive: bool):
    Find the hero by ID
    If hero not found, return 404
    Get the hero's allies list
    Convert ally IDs to full hero objects
    If include_inactive is False, filter out inactive allies
    Return the allies
```

**Implementation hints:**
```python
@app.get("/heroes/{hero_id}/allies")
async def get_hero_allies(
    hero_id: int = Path(..., ge=1),
    include_inactive: bool = Query(True)
):
    """Get the allies of a specific hero."""
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
                    allies.append(h)
                break
    
    return {
        "hero": hero["name"],
        "ally_count": len(allies),
        "allies": allies
    }
```

## Validation and Error Handling

Always validate your inputs and provide clear error messages. FastAPI makes this easy with its built-in validation:

```python
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
    # Implementation...
```

Use HTTP exceptions for appropriate status codes:

```python
if not hero:
    raise HTTPException(
        status_code=404,
        detail=f"Hero with ID {hero_id} not found"
    )
```

## For the Knightfall Protocol (Push Harder Challenge)

### Implementing Pagination

For all list endpoints, consider implementing pagination like this:

```python
@app.get("/heroes/")
async def list_heroes(
    # Other parameters...
    sort_by: Optional[str] = Query(None, enum=["name", "power_level", "city"]),
    sort_dir: Optional[str] = Query("asc", enum=["asc", "desc"]),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    results = # Your filtered results...
    
    # Apply sorting if requested
    if sort_by:
        reverse = sort_dir.lower() == "desc"
        if sort_by == "name":
            results.sort(key=lambda x: x["name"], reverse=reverse)
        elif sort_by == "power_level":
            results.sort(key=lambda x: x["power_level"], reverse=reverse)
        elif sort_by == "city":
            results.sort(key=lambda x: x["base_city"], reverse=reverse)
    
    # Get total count before pagination
    total = len(results)
    
    # Apply pagination
    results = results[offset:offset + limit]
    
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "heroes": results
    }
```

### Implementing a Full-Text Search

```python
@app.get("/heroes/fulltext")
async def fulltext_search(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Full-text search across hero records.
    Searches in name, real_name, city, and powers.
    """
    q = q.lower()
    results = []
    
    for hero in heroes_db:
        # Check if query appears in any searchable field
        if (
            q in hero["name"].lower() or
            q in hero["real_name"].lower() or
            q in hero["base_city"].lower() or
            any(q in power.lower() for power in hero["powers"])
        ):
            # Add relevance score based on where it matched
            hero_copy = hero.copy()
            hero_copy["relevance"] = 0
            
            if q in hero["name"].lower():
                hero_copy["relevance"] += 3  # Name matches are most important
            
            if q in hero["real_name"].lower():
                hero_copy["relevance"] += 2
            
            if q in hero["base_city"].lower():
                hero_copy["relevance"] += 1
            
            # Add 1 for each power match
            for power in hero["powers"]:
                if q in power.lower():
                    hero_copy["relevance"] += 1
            
            results.append(hero_copy)
    
    # Sort by relevance
    results.sort(key=lambda x: x["relevance"], reverse=True)
    
    # Get total before pagination
    total = len(results)
    
    # Apply pagination
    results = results[offset:offset + limit]
    
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "heroes": results
    }
```

Remember: A well-designed API is like Batman's utility belt - it should have specialized tools for common tasks while remaining flexible enough to handle unexpected situations.
