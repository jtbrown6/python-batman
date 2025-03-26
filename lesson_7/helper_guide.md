# Bruce Wayne's Journal: Arkham Asylum Management API

## Thought Process for Request Bodies and Pydantic Models

When designing the Arkham Asylum Management API, I needed a robust system to ensure accurate, validated data. After all, incorrect information about an inmate like Joker or Scarecrow could lead to catastrophic outcomes. Pydantic models provide the precision and validation I need for this critical application.

### 1. Planning the Model Architecture

**Thought process:**
- Need to represent complex entities: inmates, staff, treatments, incidents
- Need validation to enforce business rules and data quality
- Need to establish clear relationships between entities
- Want to handle both input (create/update) and output (retrieve) scenarios
- Need to build a hierarchy of models for code reuse and consistency

**Solution approach:**
- Create base models for shared attributes
- Define specialized models for specific operations
- Implement validation rules through Pydantic fields and validators
- Design clear class hierarchies with inheritance
- Use response models to control API output

### 2. Implementing Enums and Base Models

**Thought process:**
- Some fields should only accept specific values (like cell blocks)
- Many entities share common fields (like name)
- Need to standardize validation and default values

**Implementation hints:**
```python
from enum import Enum
from pydantic import BaseModel, Field

class CellBlock(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

class PersonBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    age: Optional[int] = Field(None, ge=18, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether the person is active in Arkham")
```

### 3. Creating Request and Response Models

**Thought process:**
- Input models need validation for user-provided data
- Output models should include system-generated fields
- Need to control which fields are visible/required in different contexts

**Implementation hints:**
```python
class InmateCreate(PersonBase):
    """Model for creating a new inmate (no ID)"""
    alias: str = Field(..., min_length=1, max_length=50, description="Criminal alias/persona")
    danger_level: int = Field(..., ge=1, le=10, description="Threat level from 1-10")
    disorders: List[str] = Field([], description="Diagnosed psychological disorders")
    cell_block: CellBlock = Field(CellBlock.D, description="Assigned cell block in Arkham")
    notes: Optional[str] = Field(None, description="Clinical observations and notes")
    
    @validator('alias')
    def alias_cannot_be_batman(cls, v):
        if v.lower() == "batman":
            raise ValueError("No inmate can claim to be Batman")
        return v

class InmateResponse(PersonBase):
    """Model for returning inmate data (includes ID)"""
    id: int
    alias: str
    danger_level: int
    disorders: List[str]
    cell_block: CellBlock
    admission_date: date
    release_date: Optional[date] = None
    notes: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Edward Nygma",
                "age": 39,
                "alias": "Riddler",
                "danger_level": 7,
                "disorders": ["Narcissistic Personality Disorder", "Obsessive-Compulsive Disorder"],
                "cell_block": "B",
                "admission_date": "2023-01-15",
                "release_date": None,
                "is_active": True,
                "notes": "Exhibits obsession with riddles and puzzles."
            }
        }
```

### 4. Implementing Update Models

**Thought process:**
- Updates should allow partial data (only fields that need to change)
- Need to maintain validation rules for updated fields
- Should handle required vs. optional fields appropriately

**Implementation hints:**
```python
class InmateUpdate(BaseModel):
    """Model for updating an inmate (all fields optional)"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=18, le=120)
    alias: Optional[str] = Field(None, min_length=1, max_length=50)
    danger_level: Optional[int] = Field(None, ge=1, le=10)
    disorders: Optional[List[str]] = None
    cell_block: Optional[CellBlock] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None
    
    @validator('alias')
    def alias_cannot_be_batman(cls, v):
        if v is not None and v.lower() == "batman":
            raise ValueError("No inmate can claim to be Batman")
        return v
```

### 5. Building Nested Models for Relationships

**Thought process:**
- Need to represent complex relationships between entities
- Want to embed related data for convenient access
- Need to maintain separation of concerns

**Implementation hints:**
```python
class TreatmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10)
    success_rate: float = Field(..., ge=0.0, le=1.0)

class TreatmentRecord(BaseModel):
    treatment_id: int
    date_assigned: date
    date_completed: Optional[date] = None
    notes: Optional[str] = None
    progress: int = Field(0, ge=0, le=10, description="Treatment progress from 0-10")
    
    @validator('date_completed')
    def completion_date_after_assigned(cls, v, values):
        if v is not None and 'date_assigned' in values and v < values['date_assigned']:
            raise ValueError('Completion date cannot be before assignment date')
        return v

class InmateWithTreatments(InmateResponse):
    """Extended model that includes treatment records"""
    treatment_records: List[TreatmentRecord] = []
```

### 6. Implementing Endpoints with Request Bodies

**Thought process:**
- Need to receive and validate complex data through request bodies
- Need to return appropriate status codes and response models
- Want to handle errors gracefully with clear messages

**Implementation hints:**
```python
@app.post("/inmates/", response_model=InmateResponse, status_code=status.HTTP_201_CREATED)
async def create_inmate(inmate: InmateCreate):
    """Add a new inmate to Arkham Asylum."""
    # Generate new ID
    new_id = max(inmate["id"] for inmate in inmates_db) + 1
    
    # Create new inmate record
    inmate_dict = inmate.dict()
    inmate_dict["id"] = new_id
    inmate_dict["admission_date"] = date.today()
    
    inmates_db.append(inmate_dict)
    
    return inmate_dict

@app.put("/inmates/{inmate_id}", response_model=InmateResponse)
async def update_inmate(
    inmate_id: int = Path(..., ge=1, description="The ID of the inmate to update"),
    inmate_data: InmateUpdate = Body(...)
):
    """Update an inmate's information."""
    # Find the inmate
    for i, inmate in enumerate(inmates_db):
        if inmate["id"] == inmate_id:
            # Update with provided fields
            update_data = inmate_data.dict(exclude_unset=True)
            inmates_db[i].update(update_data)
            return inmates_db[i]
    
    raise HTTPException(status_code=404, detail=f"Inmate {inmate_id} not found")
```

### 7. Using Response Models for Consistent Output

**Thought process:**
- Want to ensure consistent API output regardless of internal data format
- Need to exclude sensitive information in some contexts
- Want to customize the response structure for different use cases

**Implementation hints:**
```python
@app.get(
    "/inmates/{inmate_id}", 
    response_model=InmateResponse
)
async def get_inmate(inmate_id: int):
    """Get a specific inmate by ID."""
    for inmate in inmates_db:
        if inmate["id"] == inmate_id:
            return inmate
    
    raise HTTPException(status_code=404, detail=f"Inmate {inmate_id} not found")

@app.get(
    "/inmates/{inmate_id}/public", 
    response_model=InmateResponse,
    response_model_exclude={"notes", "disorders"}
)
async def get_inmate_public_info(inmate_id: int):
    """Get the public information about an inmate (excludes sensitive data)."""
    for inmate in inmates_db:
        if inmate["id"] == inmate_id:
            return inmate
    
    raise HTTPException(status_code=404, detail=f"Inmate {inmate_id} not found")
```

## For the Knightfall Protocol (Push Harder Challenge)

### Complex Nested Data Structures

```python
class Location(BaseModel):
    building: str = Field(..., min_length=2)
    wing: str = Field(..., min_length=1)
    cell_number: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "building": "Main Asylum",
                "wing": "East Wing",
                "cell_number": "A-13"
            }
        }

class CaseFile(BaseModel):
    """Comprehensive case file with detailed inmate info"""
    inmate: InmateResponse
    psychological_profile: str = Field(..., min_length=10)
    threat_assessment: str = Field(..., min_length=10)
    escape_attempts: int = Field(0, ge=0)
    known_associates: List[str] = []
    treatment_history: List[TreatmentRecord] = []
    incidents: List[Incident] = []
    location: Location
    
    class Config:
        schema_extra = {
            "example": {
                "inmate": {
                    "id": 1,
                    "name": "Edward Nygma",
                    "alias": "Riddler",
                    # ...other inmate fields
                },
                "psychological_profile": "Exhibits narcissistic tendencies with obsessive behaviors...",
                "threat_assessment": "High intelligence makes him a significant escape risk...",
                "escape_attempts": 3,
                "known_associates": ["Penguin", "Mad Hatter"],
                # ...other fields with examples
            }
        }
```

### Generic Response Models

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class ResponseBase(Generic[T]):
    """Generic response wrapper with metadata"""
    data: Optional[T] = None
    success: bool = True
    message: str = "Operation completed successfully"
    errors: List[str] = []

class PaginatedResponse(Generic[T]):
    """Paginated response for list endpoints"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    @validator('pages')
    def compute_pages(cls, v, values):
        if v is None and 'total' in values and 'size' in values and values['size'] > 0:
            return (values['total'] + values['size'] - 1) // values['size']
        return v

# Usage:
@app.get("/inmates/", response_model=PaginatedResponse[InmateResponse])
async def list_inmates(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    """List inmates with pagination."""
    # Calculate pagination
    start = (page - 1) * size
    end = start + size
    
    items = inmates_db[start:end]
    total = len(inmates_db)
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }
```

### Custom Validators for Domain Logic

```python
class InmateTransfer(BaseModel):
    inmate_id: int
    destination: str
    reason: str
    security_level: int = Field(..., ge=1, le=5)
    escort_size: int = Field(2, ge=1, le=10)
    
    @validator('escort_size')
    def validate_escort_size(cls, v, values):
        # Ensure high-security inmates get larger escorts
        if 'security_level' in values:
            if values['security_level'] >= 4 and v < 4:
                raise ValueError(f"Security level {values['security_level']} requires at least 4 escorts")
        return v
    
    @validator('destination')
    def no_blackgate_for_special_cases(cls, v, values):
        if v.lower() == "blackgate prison" and 'inmate_id' in values:
            # Lookup the inmate
            inmate = next((i for i in inmates_db if i["id"] == values['inmate_id']), None)
            if inmate and inmate.get('alias') in ["Joker", "Riddler", "Scarecrow", "Poison Ivy"]:
                raise ValueError(f"{inmate['alias']} cannot be transferred to Blackgate due to special containment needs")
        return v
```

Remember, even the most dangerous inmates deserve precise, validated records. As Batman, I ensure that Arkham's systems are as meticulous as my own crime-fighting preparations.
