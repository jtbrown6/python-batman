# Lesson 7: Arkham Records (Request Bodies & Pydantic Models)

## The Arkham Files

Just as Batman maintains meticulous records on Arkham Asylum's inmates, ensuring each detail is accurate and validated, FastAPI uses Pydantic models to enforce data integrity in your API. In this lesson, we'll dive deep into request bodies and data validation with Pydantic.

## Why Request Bodies Matter

In previous lessons, we worked with path and query parameters, which are great for simple data. However, there are important limitations:

1. **Size constraints** - URLs have length limits, making them unsuitable for complex data
2. **Data types** - Path/query parameters are primarily strings with simple conversions
3. **Structure** - They don't easily represent nested data structures
4. **Security** - Sensitive data shouldn't be in URLs where it's visible and logged

Request bodies solve these problems by:
- Allowing transmission of complex, structured data
- Supporting rich data types and nested objects
- Keeping sensitive data out of URLs and server logs
- Enabling comprehensive validation rules

## Why Pydantic is Powerful

Pydantic is a data validation and settings management library used by FastAPI. It provides:

1. **Type enforcement** - Ensures data matches expected types
2. **Data validation** - Applies rules to validate data beyond just types
3. **Automatic documentation** - Generates OpenAPI schemas for your models
4. **IDE support** - Provides autocomplete and type hints in your editor
5. **Error handling** - Generates clear, specific error messages

Think of Pydantic as Batman's detective skills - automatically spotting inconsistencies and ensuring everything is in perfect order before accepting it.

## Learning Objectives
- Create Pydantic models for request and response data
- Implement field validation with various constraints
- Design model hierarchies with inheritance
- Set up relationships between models
- Handle nested data structures
- Use response models to standardize API outputs

## Creating Basic Pydantic Models

Let's start with a basic model for inmates at Arkham Asylum:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Inmate(BaseModel):
    id: Optional[int] = None
    name: str
    alias: str
    danger_level: int = Field(..., ge=1, le=10)
    incarceration_date: date
    is_active: bool = True
    disorders: List[str] = []

app = FastAPI()

@app.post("/inmates/")
async def create_inmate(inmate: Inmate):
    """Create a new inmate record."""
    # In a real app, we would save to a database
    return {"message": "Inmate recorded", "inmate": inmate}
```

Key elements to understand:
- **Field types**: Each field has a type annotation (`str`, `int`, `date`, etc.)
- **Default values**: Fields can have defaults (like `is_active = True`)
- **Field customization**: The `Field` function provides validation and metadata
- **Type imports**: `List` and `Optional` from typing are used for complex types

## Testing with FastAPI's Docs UI

With just this code, FastAPI automatically:
1. Creates a JSON Schema for your model
2. Validates incoming requests against that schema
3. Converts data types (e.g., string to date)
4. Documents the schema in OpenAPI
5. Creates an interactive form in the Swagger UI

To test it, run your app and go to http://127.0.0.1:8000/docs, where you'll see a form to create an inmate with appropriate fields and validation.

## Field Validation with Pydantic

Pydantic offers extensive validation options through the `Field` function:

```python
class Inmate(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier")
    name: str = Field(..., min_length=2, max_length=50, description="Inmate's real name")
    alias: str = Field(..., min_length=1, max_length=50, description="Inmate's criminal alias")
    danger_level: int = Field(..., ge=1, le=10, description="Threat level from 1-10")
    incarceration_date: date = Field(..., description="Date of imprisonment")
    is_active: bool = Field(True, description="Whether inmate is currently in Arkham")
    disorders: List[str] = Field([], description="Diagnosed psychological disorders")
    cell_block: str = Field("D", description="Arkham wing assignment", regex="^[A-D]$")
```

Common validation parameters:
- `...` - Ellipsis indicating the field is required
- `ge`, `le`, `gt`, `lt` - Greater/less than (or equal)
- `min_length`, `max_length` - String length constraints
- `regex` - Regular expression pattern matching
- `description` - Field documentation

## Custom Validations

Sometimes the built-in validations aren't enough. Pydantic allows custom validators:

```python
from pydantic import BaseModel, Field, validator

class Inmate(BaseModel):
    id: Optional[int] = None
    name: str
    alias: str
    danger_level: int = Field(..., ge=1, le=10)
    notes: Optional[str] = None
    
    @validator('name')
    def name_must_not_be_villain(cls, v):
        if v.lower() == "joker":
            raise ValueError("Real name cannot be 'Joker'")
        return v.title()
    
    @validator('notes', always=True)
    def set_notes_default(cls, v, values):
        if v is None:
            return f"Inmate {values.get('name', 'Unknown')} has no additional notes."
        return v
```

Key validator features:
- **@validator decorator** - Specifies which field(s) this validates
- **always=True** - Run even if the field is None
- **values** - Access to other fields already validated
- **Return the value** - You can transform data, not just validate

## Model Inheritance and Hierarchies

Just as Batman categorizes Gotham's villains, we can create model hierarchies:

```python
class PersonBase(BaseModel):
    name: str
    age: Optional[int] = None
    
class InmateBase(PersonBase):
    alias: str
    danger_level: int = Field(..., ge=1, le=10)
    
class InmateIn(InmateBase):
    """Model used for creating inmates (no ID)"""
    disorders: List[str] = []
    
class InmateOut(InmateBase):
    """Model used for returning inmates (includes ID)"""
    id: int
    disorders: List[str] = []
    added_date: date
    
class InmateUpdate(BaseModel):
    """Model for updates (all fields optional)"""
    name: Optional[str] = None
    age: Optional[int] = None
    alias: Optional[str] = None
    danger_level: Optional[int] = Field(None, ge=1, le=10)
    disorders: Optional[List[str]] = None
```

Benefits of this approach:
- **Reuse common fields** - Avoid duplicating field definitions
- **API clarity** - Different models for different operations
- **Type safety** - Each endpoint uses the appropriate model
- **Consistent validation** - Core rules apply across model variations

## Working with Model Relationships

In real applications, models often relate to each other:

```python
class Therapy(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    success_rate: float = Field(..., ge=0.0, le=1.0)

class TherapyRecord(BaseModel):
    therapy_id: int
    inmate_id: int
    date: date
    notes: str
    progress: int = Field(..., ge=0, le=5)

class InmateWithTherapies(InmateOut):
    """Inmate with their therapy records"""
    therapy_records: List[TherapyRecord] = []
```

A common pattern is to extend base models with relationship data:

```python
@app.get("/inmates/{inmate_id}", response_model=InmateWithTherapies)
async def get_inmate_with_therapies(inmate_id: int):
    # Get inmate data
    inmate = find_inmate(inmate_id)
    
    # Get therapy records
    therapy_records = get_therapy_records(inmate_id)
    
    # Combine them
    inmate["therapy_records"] = therapy_records
    
    return inmate
```

## Nested Models and Complex Data

Batman's records often contain complex, nested data. Pydantic handles this elegantly:

```python
class Address(BaseModel):
    street: str
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., regex="^\\d{5}(-\\d{4})?$")

class Incident(BaseModel):
    date: date
    description: str
    victims: Optional[int] = Field(0, ge=0)
    location: Optional[Address] = None

class CriminalProfile(BaseModel):
    specialties: List[str] = []
    modus_operandi: str
    psychological_profile: str
    known_incidents: List[Incident] = []
    known_hideouts: List[Address] = []

class InmateDetail(InmateOut):
    criminal_profile: Optional[CriminalProfile] = None
```

This creates a rich, hierarchical model structure that can represent complex relationships.

## Response Models: Controlling Output

By default, FastAPI uses the return value's structure. With `response_model`, you can:
- Enforce schema validation on responses
- Remove fields you don't want to expose
- Ensure consistent output structure

```python
@app.get(
    "/inmates/{inmate_id}", 
    response_model=InmateOut,
    response_model_exclude_unset=True  # Only include fields that were explicitly set
)
async def get_inmate(inmate_id: int):
    # Get inmate data from database
    inmate = find_inmate(inmate_id)
    
    # This ensures only fields in InmateOut are returned,
    # regardless of what's in the database record
    return inmate

@app.get(
    "/inmates/{inmate_id}/secure", 
    response_model=InmateOut,
    response_model_exclude={"disorders", "notes"}  # Exclude sensitive fields
)
async def get_inmate_limited(inmate_id: int):
    inmate = find_inmate(inmate_id)
    return inmate
```

Response model options:
- **response_model_exclude_unset** - Only include non-default values
- **response_model_exclude_defaults** - Exclude fields set to their default
- **response_model_exclude_none** - Exclude fields set to None
- **response_model_exclude** - Exclude specific fields
- **response_model_include** - Include only specific fields

## Field Aliases and JSON Names

Sometimes your Python field names differ from the JSON keys you want:

```python
class Inmate(BaseModel):
    inmate_id: int = Field(..., alias="id")
    full_name: str = Field(..., alias="name")
    
    class Config:
        # Allow using aliases when creating from dict
        allow_population_by_field_name = True
        
        # Customize JSON schema properties
        schema_extra = {
            "example": {
                "id": 123,
                "name": "Edward Nygma",
                "alias": "Riddler"
            }
        }
```

This allows you to use pythonic names in your code while maintaining different JSON structure.

## Project: Arkham Asylum Management API

Your mission is to create a comprehensive API for Arkham Asylum's records. The system should:

1. Define Pydantic models for inmates, staff, incidents, and therapies
2. Create endpoints for adding, retrieving, and updating asylum records
3. Implement validation for all data fields
4. Use model relationships to connect entities
5. Add response models to standardize API outputs

Create a file named `arkham_api.py` using the starter code provided.

## The Knightfall Protocol (Push Harder Challenge)

Enhance your Arkham Asylum API to:
1. Implement complex nested data structures for case files
2. Add custom validators for domain-specific rules
3. Create model hierarchies with inheritance
4. Implement generic responses (success/error) with type hints
5. Add example data for testing and documentation

## Resources

- Check out `starter_code.py` to get started
- If you need guidance, look at the `helper_guide.md` file for "Bruce Wayne's Journal"
- After you've tried solving it yourself, you can check `solution.py` for one possible implementation

Remember, in the words of Batman: "It's not just about catching the criminals, but maintaining the detailed records that help us stay one step ahead."
