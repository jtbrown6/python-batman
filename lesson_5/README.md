# Lesson 5: Batcomputer Database (FastAPI Basics)

## Welcome to the Batcomputer!

Just as Batman needed to build the Batcomputer to organize his crime-fighting data, we need a system to manage and share information through a web API. In this lesson, we'll start building a RESTful API using FastAPI - a modern, high-performance Python web framework.

## Why APIs Matter

Before diving into FastAPI, let's understand why APIs (Application Programming Interfaces) are so important:

1. **Data Sharing**: APIs allow different systems to share data - like how Batman shares information with Gordon or Alfred
2. **Service Integration**: They enable connecting various services - just as Batman connects the Batcomputer to his vehicles and gadgets
3. **Frontend/Backend Separation**: APIs let us build separate frontend and backend systems - like how Batman's interface is separate from the powerful computing hardware
4. **Scalability**: Well-designed APIs handle growth better - the Batcomputer started small but expanded over time

REST (Representational State Transfer) APIs have become the standard for web services because they're:
- Stateless (each request contains all information needed)
- Cacheable (responses can be stored for performance)
- Uniform interface (consistent access to resources)
- Based on standard HTTP methods (GET, POST, PUT, DELETE)

## Why FastAPI?

Batman always chooses the best tools for the job, and for Python web APIs, FastAPI stands out because:

1. **Speed**: One of the fastest Python frameworks available - because when you're fighting crime, every millisecond counts
2. **Automatic Documentation**: Generates API docs automatically - like how Batman documents all his gadgets
3. **Modern Python Features**: Uses type hints, async/await - leveraging Python's newest capabilities
4. **Easy to Learn**: Intuitive API with minimal boilerplate code - get up and running quickly
5. **Robust Validation**: Automatic request validation with Pydantic - preventing errors before they occur

## Learning Objectives
- Understand REST API concepts and why they're valuable
- Set up a FastAPI application and run it with Uvicorn
- Create basic API endpoints with path operations
- Test your API using the auto-generated Swagger UI (/docs)
- Implement standard HTTP methods (GET, POST, PUT, DELETE)

## Installing FastAPI and Uvicorn

First, we need to install the necessary packages. Uvicorn is an ASGI server that will run our FastAPI application:

```bash
pip install fastapi uvicorn
```

## Creating Your First FastAPI Application

Let's create a simple FastAPI application for the Batcomputer:

```python
from fastapi import FastAPI

# Initialize the Batcomputer API
app = FastAPI(
    title="Batcomputer API",
    description="Access to Batman's criminal database and Gotham City information",
    version="1.0.0"
)

# Root endpoint - the entry point to our API
@app.get("/")
async def batcomputer_welcome():
    """Return a welcome message for the Batcomputer API."""
    return {"message": "Welcome to the Batcomputer. Authorize to proceed."}
```

Let's break down what's happening:

1. **Importing FastAPI**: We import the `FastAPI` class from the `fastapi` package
2. **Creating an Application**: We create an instance of `FastAPI` with metadata
3. **Defining an Endpoint**: We use a decorator `@app.get("/")` to define a route
4. **Handler Function**: We create a function that returns data (automatically converted to JSON)

## Running Your FastAPI Application

Let's save the above code to a file named `main.py` and run it with Uvicorn:

```bash
uvicorn main:app --reload
```

Explanation:
- `main`: The name of the Python file
- `app`: The name of the FastAPI instance in the file
- `--reload`: Automatically reload when code changes (great for development)

Once running, you can access:
- Your API at http://127.0.0.1:8000
- Auto-generated Swagger UI at http://127.0.0.1:8000/docs
- Alternative ReDoc documentation at http://127.0.0.1:8000/redoc

## Understanding Path Operations

In FastAPI, routes are created using "path operation decorators" that correspond to HTTP methods:

```python
@app.get("/criminals/")  # HTTP GET request
async def list_criminals():
    """Get a list of known criminals in Gotham."""
    return [
        {"id": 1, "name": "Joker", "status": "At large"},
        {"id": 2, "name": "Penguin", "status": "In custody"},
        {"id": 3, "name": "Riddler", "status": "Unknown"}
    ]

@app.get("/criminals/{criminal_id}")  # Path parameter
async def get_criminal(criminal_id: int):
    """Get details about a specific criminal by ID."""
    # In a real API, we would fetch this from a database
    criminals = {
        1: {"id": 1, "name": "Joker", "status": "At large", "threat_level": "Extreme"},
        2: {"id": 2, "name": "Penguin", "status": "In custody", "threat_level": "High"},
        3: {"id": 3, "name": "Riddler", "status": "Unknown", "threat_level": "High"}
    }
    
    if criminal_id not in criminals:
        # We'll learn better error handling later
        return {"error": "Criminal not found"}
    
    return criminals[criminal_id]
```

Key concepts to understand:
- **Path Operation Decorators**: `@app.get()`, `@app.post()`, `@app.put()`, `@app.delete()`
- **Path Parameters**: Variables in the path like `{criminal_id}`
- **Type Annotations**: `criminal_id: int` tells FastAPI to convert and validate
- **Async Support**: Using `async def` for asynchronous functions (optional but recommended)

## Query Parameters

Query parameters are included in the URL after a `?` symbol:

```python
# /criminals/search?name=joker&status=at%20large
@app.get("/criminals/search")
async def search_criminals(name: str = None, status: str = None):
    """Search for criminals by name and/or status."""
    criminals = [
        {"id": 1, "name": "Joker", "status": "At large"},
        {"id": 2, "name": "Penguin", "status": "In custody"},
        {"id": 3, "name": "Riddler", "status": "Unknown"}
    ]
    
    results = criminals.copy()
    
    if name:
        results = [c for c in results if name.lower() in c["name"].lower()]
    
    if status:
        results = [c for c in results if status.lower() in c["status"].lower()]
    
    return results
```

Important points:
- Query parameters are automatically extracted from function parameters
- Default values make parameters optional
- Type annotations provide automatic validation
- Documentation is automatically generated

## Creating Resources with POST

To create new resources, we use the HTTP POST method:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define a model for our data with Pydantic
class Criminal(BaseModel):
    name: str
    status: str
    threat_level: str = "Unknown"  # Optional with default

# This would typically be a database
criminals_db = [
    {"id": 1, "name": "Joker", "status": "At large", "threat_level": "Extreme"},
    {"id": 2, "name": "Penguin", "status": "In custody", "threat_level": "High"}
]

@app.post("/criminals/", status_code=201)  # 201 Created
async def create_criminal(criminal: Criminal):
    """Add a new criminal to the database."""
    # Generate new ID (in a real app, the database would do this)
    new_id = max(c["id"] for c in criminals_db) + 1
    
    # Create new criminal dict with ID
    new_criminal = criminal.dict()
    new_criminal["id"] = new_id
    
    # Add to our "database"
    criminals_db.append(new_criminal)
    
    return new_criminal
```

What's happening:
1. We define a Pydantic model to validate the request body
2. FastAPI automatically validates incoming JSON against this model
3. We return the created resource with a 201 status code
4. The data is automatically converted to JSON

## Updating Resources with PUT

For updates, we use the HTTP PUT method:

```python
@app.put("/criminals/{criminal_id}")
async def update_criminal(criminal_id: int, criminal: Criminal):
    """Update an existing criminal's information."""
    # Find the criminal by ID
    for i, c in enumerate(criminals_db):
        if c["id"] == criminal_id:
            # Update the criminal, preserving the ID
            criminals_db[i] = {**criminal.dict(), "id": criminal_id}
            return criminals_db[i]
    
    # If we get here, the criminal wasn't found
    raise HTTPException(status_code=404, detail="Criminal not found")
```

Important concepts:
1. We use `HTTPException` for proper error responses
2. We preserve the ID while updating other fields
3. The function returns the updated resource

## Deleting Resources with DELETE

For deletion, we use the HTTP DELETE method:

```python
@app.delete("/criminals/{criminal_id}")
async def delete_criminal(criminal_id: int):
    """Remove a criminal from the database."""
    # Find the criminal by ID
    for i, c in enumerate(criminals_db):
        if c["id"] == criminal_id:
            # Remove from the list
            deleted = criminals_db.pop(i)
            return {"message": f"Criminal {deleted['name']} deleted"}
    
    # If we get here, the criminal wasn't found
    raise HTTPException(status_code=404, detail="Criminal not found")
```

## Testing with Swagger UI (/docs)

One of FastAPI's most powerful features is the automatic Swagger UI documentation:

1. Run your application with `uvicorn main:app --reload`
2. Open http://127.0.0.1:8000/docs in your browser
3. You'll see all your endpoints documented with:
   - HTTP methods
   - URLs
   - Parameters
   - Request body schemas
   - Response schemas
   - Authentication (when configured)

You can actually test your API directly from this UI:
1. Click on any endpoint to expand it
2. Click "Try it out"
3. Fill in any parameters or request body
4. Click "Execute"
5. See the response, including status code and response body

Think of this as Batman's control panel for testing all the Batcomputer's functions!

## Project: Batcomputer Criminal Database API

Your mission is to create a complete RESTful API for managing Batman's criminal database. The system should:

1. Define endpoints for listing, retrieving, creating, updating, and deleting criminals
2. Use Pydantic models for data validation
3. Implement proper error handling with HTTP exceptions
4. Include query parameters for searching and filtering criminals

Create a file named `criminal_api.py` using the starter code provided.

## The Knightfall Protocol (Push Harder Challenge)

Enhance your Batcomputer API to:
1. Add additional data models for crimes, evidence, and locations
2. Implement relationships between criminals and their crimes
3. Add path parameters for filtering (e.g., by threat level)
4. Implement advanced search functionality with multiple parameters

## Resources

- Check out `starter_code.py` to get started
- If you need guidance, look at the `helper_guide.md` file for "Bruce Wayne's Journal"
- After you've tried solving it yourself, you can check `solution.py` for one possible implementation

Remember, in the words of Batman: "It's not just what I build, but how I use it that defines me."
