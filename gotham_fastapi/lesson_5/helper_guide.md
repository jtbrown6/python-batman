# Bruce Wayne's Journal: Batcomputer Criminal Database API

## Thought Process for Building a RESTful API

When I designed the Batcomputer's API interface, I approached it methodically, breaking down the problem into manageable components and thinking through each decision carefully.

### 1. Data Modeling with Pydantic

**Thought process:**
- Need to define what a "criminal" record looks like in a structured way
- Need validation to prevent bad data from entering our system
- Should consider which fields are required vs. optional
- Should consider relationships between different data entities

**Solution approach:**
- Use Pydantic's BaseModel to create a validated data model
- Define required fields without defaults (name, status)
- Define optional fields with defaults (threat_level)
- Add validators where needed for custom rules

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class Criminal(BaseModel):
    name: str
    status: str
    threat_level: str = "Unknown"  # Optional with default
    last_known_location: Optional[str] = None
    psycho_profile: Optional[str] = None
    
    # For the Knightfall Protocol enhancement
    # known_associates: List[str] = []
    # crimes: List[str] = []
```

### 2. API Endpoint Design

**Thought process:**
- Need endpoints for all CRUD operations (Create, Read, Update, Delete)
- Need to organize endpoints in a logical structure
- Need to consider how to handle errors gracefully
- Should follow RESTful principles for consistency

**Solution approach:**
- Create endpoints for each operation on the criminals resource
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Structure URLs according to REST conventions
- Use proper status codes (200, 201, 404, etc.)

```
GET /criminals/           - List all criminals
GET /criminals/{id}       - Get a specific criminal
GET /criminals/search     - Search for criminals
POST /criminals/          - Create a new criminal
PUT /criminals/{id}       - Update a criminal
DELETE /criminals/{id}    - Delete a criminal
```

### 3. Implementation of GET Endpoints

**Thought process:**
- Need to return a list of all criminals for the index endpoint
- Need to find and return a specific criminal by ID
- Need to handle the case where a criminal doesn't exist
- Should support filtering and searching

**Pseudo-code for key functions:**
```
Function list_criminals():
    Return the entire criminals database list
    
Function get_criminal(criminal_id):
    Search for the criminal with matching ID
    If found, return the criminal data
    If not found, return a 404 error
    
Function search_criminals(name, status, threat_level):
    Start with a copy of all criminals
    If name parameter provided, filter by name
    If status parameter provided, filter by status
    If threat_level parameter provided, filter by threat level
    Return the filtered list
```

### 4. Implementation of POST Endpoint

**Thought process:**
- Need to validate incoming data against our model
- Need to generate a new unique ID
- Need to add the new criminal to our database
- Should return the newly created criminal with its ID

**Pseudo-code:**
```
Function create_criminal(criminal_data):
    Validate criminal_data against our Criminal model
    Generate a new unique ID
    Create a complete criminal record with the ID
    Add the record to our database
    Return the created record with a 201 status code
```

### 5. Implementation of PUT Endpoint

**Thought process:**
- Need to validate incoming data against our model
- Need to find the existing criminal by ID
- Need to update the criminal's information
- Should handle the case where the criminal doesn't exist

**Pseudo-code:**
```
Function update_criminal(criminal_id, criminal_data):
    Validate criminal_data against our Criminal model
    Find the criminal with matching ID
    If not found, return a 404 error
    Update the criminal's information while preserving the ID
    Return the updated record
```

### 6. Implementation of DELETE Endpoint

**Thought process:**
- Need to find the criminal by ID
- Need to remove them from the database
- Should handle the case where the criminal doesn't exist
- Should return confirmation of deletion

**Pseudo-code:**
```
Function delete_criminal(criminal_id):
    Find the criminal with matching ID
    If not found, return a 404 error
    Remove the criminal from the database
    Return a confirmation message
```

## Implementation Hints

### Pydantic Model:
```python
from pydantic import BaseModel, Field
from typing import Optional, List

class Criminal(BaseModel):
    name: str
    status: str
    threat_level: str = "Unknown"
    last_known_location: Optional[str] = None
    psycho_profile: Optional[str] = None
```

### GET Endpoints:
```python
@app.get("/criminals/")
async def list_criminals():
    return criminals_db

@app.get("/criminals/{criminal_id}")
async def get_criminal(criminal_id: int):
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
    results = criminals_db.copy()
    
    if name:
        results = [c for c in results if name.lower() in c["name"].lower()]
    
    if status:
        results = [c for c in results if status.lower() in c["status"].lower()]
    
    if threat_level:
        results = [c for c in results if threat_level.lower() == c["threat_level"].lower()]
    
    return results
```

### POST Endpoint:
```python
@app.post("/criminals/", status_code=201)
async def create_criminal(criminal: Criminal):
    # Generate new ID
    new_id = max(c["id"] for c in criminals_db) + 1
    
    # Create new criminal dict with ID
    new_criminal = criminal.dict()
    new_criminal["id"] = new_id
    
    # Add to our "database"
    criminals_db.append(new_criminal)
    
    return new_criminal
```

### PUT Endpoint:
```python
@app.put("/criminals/{criminal_id}")
async def update_criminal(criminal_id: int, criminal: Criminal):
    for i, c in enumerate(criminals_db):
        if c["id"] == criminal_id:
            # Update the criminal, preserving the ID
            updated_criminal = criminal.dict()
            updated_criminal["id"] = criminal_id
            criminals_db[i] = updated_criminal
            return updated_criminal
    
    raise HTTPException(status_code=404, detail="Criminal not found")
```

### DELETE Endpoint:
```python
@app.delete("/criminals/{criminal_id}")
async def delete_criminal(criminal_id: int):
    for i, c in enumerate(criminals_db):
        if c["id"] == criminal_id:
            # Remove from the list
            deleted = criminals_db.pop(i)
            return {"message": f"Criminal {deleted['name']} deleted"}
    
    raise HTTPException(status_code=404, detail="Criminal not found")
```

## For the Knightfall Protocol (Push Harder Challenge)

### Enhanced Data Models:
```python
class Crime(BaseModel):
    name: str
    description: Optional[str] = None
    date: str
    location: str
    evidence: List[str] = []

class CriminalWithCrimes(Criminal):
    crimes: List[Crime] = []
    known_associates: List[str] = []
```

### Advanced Search:
```python
@app.get("/criminals/advanced-search")
async def advanced_search(
    name: Optional[str] = None,
    status: Optional[str] = None,
    threat_level: Optional[str] = None,
    location: Optional[str] = None,
    associated_with: Optional[str] = None
):
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
```

### Path Parameters for Filtering:
```python
@app.get("/criminals/threat-level/{level}")
async def criminals_by_threat_level(level: str):
    return [c for c in criminals_db if c["threat_level"].lower() == level.lower()]
```

### Building Relationships:
```python
@app.get("/criminals/{criminal_id}/associates")
async def get_criminal_associates(criminal_id: int):
    # Find the criminal
    for criminal in criminals_db:
        if criminal["id"] == criminal_id:
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
    
    raise HTTPException(status_code=404, detail="Criminal not found")
```

Remember, Batman's most powerful weapon isn't his gadgets, but his intellect and preparation. Similarly, in API design, careful planning and organization will serve you better than any fancy technique.
