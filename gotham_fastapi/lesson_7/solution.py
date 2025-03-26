#!/usr/bin/env python3
"""
Arkham Asylum Management API - Complete Solution
----------------------------
A fully implemented API for Arkham Asylum's records
using FastAPI with Pydantic models and request bodies.
"""
from fastapi import FastAPI, Path, Query, HTTPException, Body, status
from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional, Dict, Any, Union, TypeVar, Generic
from enum import Enum
from datetime import date, datetime
import uvicorn

# Initialize our Arkham API
app = FastAPI(
    title="Arkham Asylum API",
    description="Management system for Arkham Asylum's inmate records",
    version="1.0.0"
)

# === Enums ===
class CellBlock(str, Enum):
    """Enum for the cell blocks in Arkham Asylum."""
    A = "A"  # Maximum security
    B = "B"  # High security
    C = "C"  # Medium security
    D = "D"  # Low security


# === Base Models ===
class PersonBase(BaseModel):
    """Base model for people (inmates and staff)."""
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    age: Optional[int] = Field(None, ge=18, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether the person is currently at Arkham")


# === Inmate Models ===
class InmateBase(PersonBase):
    """Base model for inmates with common fields."""
    alias: str = Field(..., min_length=1, max_length=50, description="Criminal alias/persona")
    danger_level: int = Field(..., ge=1, le=10, description="Threat level from 1-10")
    disorders: List[str] = Field([], description="Diagnosed psychological disorders")
    cell_block: CellBlock = Field(CellBlock.D, description="Assigned cell block in Arkham")
    notes: Optional[str] = Field(None, description="Clinical observations and notes")
    
    @validator('alias')
    def alias_cannot_be_batman(cls, v):
        if v.lower() == "batman":
            raise ValueError("No inmate can claim to be Batman")
        return v.title()  # Normalize alias capitalization


class InmateCreate(InmateBase):
    """Model for creating a new inmate (no ID)."""
    pass


class InmateUpdate(BaseModel):
    """Model for updating an inmate (all fields optional)."""
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
        return v.title() if v else v


class InmateResponse(InmateBase):
    """Model for returning inmate data (includes ID)."""
    id: int
    admission_date: date
    release_date: Optional[date] = None

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


# === Staff Models ===
class StaffBase(PersonBase):
    """Base model for staff members."""
    position: str = Field(..., min_length=2, max_length=50)
    department: str = Field(..., min_length=2, max_length=50)
    

class StaffCreate(StaffBase):
    """Model for creating a new staff member."""
    assigned_inmates: List[int] = Field([], description="IDs of assigned inmates")


class StaffUpdate(BaseModel):
    """Model for updating a staff member."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=21, le=80)
    position: Optional[str] = Field(None, min_length=2, max_length=50)
    department: Optional[str] = Field(None, min_length=2, max_length=50)
    is_active: Optional[bool] = None
    assigned_inmates: Optional[List[int]] = None


class StaffResponse(StaffBase):
    """Model for returning staff data."""
    id: int
    hire_date: date
    assigned_inmates: List[int] = []


# === Treatment Models ===
class TreatmentBase(BaseModel):
    """Base model for treatment programs."""
    name: str = Field(..., min_length=2, max_length=100, description="Treatment name")
    description: str = Field(..., min_length=10, description="Treatment description")
    success_rate: float = Field(..., ge=0.0, le=1.0, description="Success rate (0-1)")


class TreatmentCreate(TreatmentBase):
    """Model for creating a new treatment."""
    pass


class TreatmentResponse(TreatmentBase):
    """Model for returning treatment data."""
    id: int


class TreatmentRecord(BaseModel):
    """Model for a treatment record (assignment of treatment to inmate)."""
    treatment_id: int
    inmate_id: int
    date_assigned: date = Field(default_factory=date.today)
    date_completed: Optional[date] = None
    notes: Optional[str] = None
    progress: int = Field(0, ge=0, le=10, description="Treatment progress from 0-10")
    
    @validator('date_completed')
    def completion_date_after_assigned(cls, v, values):
        if v is not None and 'date_assigned' in values and v < values['date_assigned']:
            raise ValueError('Completion date cannot be before assignment date')
        return v


# === Incident Models ===
class IncidentBase(BaseModel):
    """Base model for incidents at Arkham."""
    inmate_id: int
    date: date = Field(default_factory=date.today)
    incident_type: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=10)
    severity: int = Field(..., ge=1, le=10, description="Severity level 1-10")
    staff_involved: List[int] = Field([], description="IDs of staff involved")


class IncidentCreate(IncidentBase):
    """Model for creating a new incident."""
    pass


class IncidentResponse(IncidentBase):
    """Model for returning incident data."""
    id: int


# === Relationship Models ===
class InmateWithTreatments(InmateResponse):
    """Extended model that includes treatment records."""
    treatment_records: List[TreatmentRecord] = []


# === Generic Response Models (Knightfall Protocol) ===
T = TypeVar('T')

class ResponseBase(BaseModel, Generic[T]):
    """Generic response wrapper with metadata."""
    data: Optional[T] = None
    success: bool = True
    message: str = "Operation completed successfully"
    errors: List[str] = []


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response for list endpoints."""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    @root_validator
    def compute_pages(cls, values):
        if 'pages' not in values or values['pages'] is None:
            if 'total' in values and 'size' in values and values['size'] > 0:
                values['pages'] = (values['total'] + values['size'] - 1) // values['size']
        return values


# === Complex Nested Models (Knightfall Protocol) ===
class Location(BaseModel):
    """Detailed location information."""
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
    """Comprehensive case file with detailed inmate info."""
    inmate: InmateResponse
    psychological_profile: str = Field(..., min_length=10)
    threat_assessment: str = Field(..., min_length=10)
    escape_attempts: int = Field(0, ge=0)
    known_associates: List[str] = []
    treatment_history: List[TreatmentRecord] = []
    incidents: List[IncidentResponse] = []
    location: Location
    
    class Config:
        schema_extra = {
            "example": {
                "inmate": {
                    "id": 1,
                    "name": "Edward Nygma",
                    "alias": "Riddler",
                    # Other inmate fields would be here
                },
                "psychological_profile": "Exhibits narcissistic tendencies with obsessive behaviors...",
                "threat_assessment": "High intelligence makes him a significant escape risk...",
                "escape_attempts": 3,
                "known_associates": ["Penguin", "Mad Hatter"],
                # Other fields would have examples too
            }
        }


# === Sample Databases (in a real app, this would be a database) ===
inmates_db = [
    {
        "id": 1,
        "name": "Edward Nygma",
        "alias": "Riddler",
        "age": 39,
        "admission_date": "2023-01-15",
        "release_date": None,
        "danger_level": 7,
        "disorders": ["Narcissistic Personality Disorder", "Obsessive-Compulsive Disorder"],
        "cell_block": "B",
        "is_active": True,
        "notes": "Exhibits obsession with riddles and puzzles. Compulsion to leave clues."
    },
    {
        "id": 2,
        "name": "Harvey Dent",
        "alias": "Two-Face",
        "age": 42,
        "admission_date": "2022-11-02",
        "release_date": None,
        "danger_level": 8,
        "disorders": ["Dissociative Identity Disorder", "Obsession with duality"],
        "cell_block": "A",
        "is_active": True,
        "notes": "All decisions made with his coin. Extremely dangerous when coin lands on the scarred side."
    }
]

staff_db = [
    {
        "id": 1,
        "name": "Dr. Joan Leland",
        "position": "Senior Psychiatrist",
        "department": "Psychiatry",
        "hire_date": "2020-03-15",
        "is_active": True,
        "assigned_inmates": [1, 2]
    },
    {
        "id": 2,
        "name": "Aaron Cash",
        "position": "Head of Security",
        "department": "Security",
        "hire_date": "2021-07-22",
        "is_active": True,
        "assigned_inmates": []
    }
]

treatments_db = [
    {
        "id": 1,
        "name": "Cognitive Behavioral Therapy",
        "description": "Focuses on challenging and changing cognitive distortions and behaviors",
        "success_rate": 0.65
    },
    {
        "id": 2,
        "name": "Pharmacotherapy",
        "description": "Medication-based treatment to manage symptoms",
        "success_rate": 0.70
    }
]

incidents_db = [
    {
        "id": 1,
        "inmate_id": 1,
        "date": "2023-02-10",
        "incident_type": "Escape Attempt",
        "description": "Attempted to escape using a puzzle box to unlock his cell",
        "severity": 8,
        "staff_involved": [2]
    }
]

treatment_records_db = [
    {
        "id": 1,
        "treatment_id": 1,
        "inmate_id": 1,
        "date_assigned": "2023-01-20",
        "date_completed": None,
        "notes": "Initial sessions show resistance to therapy. Continues to speak in riddles.",
        "progress": 2
    },
    {
        "id": 2,
        "treatment_id": 2,
        "inmate_id": 2,
        "date_assigned": "2022-11-05",
        "date_completed": None,
        "notes": "Medication shows partial success in stabilizing mood. Still fixated on coin.",
        "progress": 4
    }
]


# === Root endpoint ===
@app.get("/")
async def read_root():
    """Welcome message for Arkham Asylum API."""
    return {
        "message": "Welcome to Arkham Asylum's Management API.",
        "endpoints": [
            "/inmates",
            "/inmates/{inmate_id}",
            "/staff",
            "/treatments",
            "/incidents"
        ]
    }


# === Inmate endpoints ===
@app.get("/inmates/", response_model=PaginatedResponse[InmateResponse])
async def list_inmates(
    active: Optional[bool] = Query(None, description="Filter by active status"),
    min_danger: Optional[int] = Query(None, ge=1, le=10, description="Minimum danger level"),
    max_danger: Optional[int] = Query(None, ge=1, le=10, description="Maximum danger level"),
    cell_block: Optional[CellBlock] = Query(None, description="Filter by cell block"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """
    List all inmates with optional filtering and pagination.
    """
    results = inmates_db.copy()
    
    # Apply filters
    if active is not None:
        results = [i for i in results if i["is_active"] == active]
    
    if min_danger is not None:
        results = [i for i in results if i["danger_level"] >= min_danger]
    
    if max_danger is not None:
        results = [i for i in results if i["danger_level"] <= max_danger]
    
    if cell_block is not None:
        results = [i for i in results if i["cell_block"] == cell_block]
    
    # Get total before pagination
    total = len(results)
    
    # Apply pagination
    start = (page - 1) * size
    end = start + size
    paginated_results = results[start:end]
    
    # Return paginated response
    return {
        "items": paginated_results,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size  # Ceiling division
    }


@app.get("/inmates/{inmate_id}", response_model=InmateResponse)
async def get_inmate(inmate_id: int = Path(..., ge=1, description="The ID of the inmate to retrieve")):
    """
    Get a specific inmate by ID.
    """
    for inmate in inmates_db:
        if inmate["id"] == inmate_id:
            return inmate
    
    raise HTTPException(status_code=404, detail=f"Inmate with ID {inmate_id} not found")


@app.post("/inmates/", response_model=InmateResponse, status_code=status.HTTP_201_CREATED)
async def create_inmate(inmate: InmateCreate):
    """
    Add a new inmate to Arkham Asylum.
    """
    # Generate new ID
    new_id = max(inmate["id"] for inmate in inmates_db) + 1 if inmates_db else 1
    
    # Create new inmate record
    inmate_dict = inmate.dict()
    inmate_dict["id"] = new_id
    inmate_dict["admission_date"] = date.today().isoformat()
    
    inmates_db.append(inmate_dict)
    
    return inmate_dict


@app.put("/inmates/{inmate_id}", response_model=InmateResponse)
async def update_inmate(
    inmate_id: int = Path(..., ge=1, description="The ID of the inmate to update"),
    inmate_data: InmateUpdate = Body(...)
):
    """
    Update an inmate's information.
    """
    # Find the inmate
    for i, inmate in enumerate(inmates_db):
        if inmate["id"] == inmate_id:
            # Extract only the set fields (exclude unset fields)
            update_data = inmate_data.dict(exclude_unset=True)
            
            # Update the inmate data
            inmates_db[i].update(update_data)
            return inmates_db[i]
    
    raise HTTPException(status_code=404, detail=f"Inmate with ID {inmate_id} not found")


@app.delete("/inmates/{inmate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inmate(inmate_id: int = Path(..., ge=1, description="The ID of the inmate to delete")):
    """
    Delete an inmate (in practice, you might want to just mark them as inactive).
    """
    for i, inmate in enumerate(inmates_db):
        if inmate["id"] == inmate_id:
            inmates_db.pop(i)
            return
    
    raise HTTPException(status_code=404, detail=f"Inmate with ID {inmate_id} not found")


# === Staff endpoints ===
@app.get("/staff/", response_model=List[StaffResponse])
async def list_staff(
    active: Optional[bool] = Query(None, description="Filter by active status"),
    department: Optional[str] = Query(None, description="Filter by department")
):
    """
    List all staff members with optional filtering.
    """
    results = staff_db.copy()
    
    # Apply filters
    if active is not None:
        results = [s for s in results if s["is_active"] == active]
    
    if department is not None:
        results = [s for s in results if department.lower() in s["department"].lower()]
    
    return results


@app.get("/staff/{staff_id}", response_model=StaffResponse)
async def get_staff_member(staff_id: int = Path(..., ge=1, description="The ID of the staff member to retrieve")):
    """
    Get a specific staff member by ID.
    """
    for staff in staff_db:
        if staff["id"] == staff_id:
            return staff
    
    raise HTTPException(status_code=404, detail=f"Staff member with ID {staff_id} not found")


@app.post("/staff/", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
async def create_staff(staff: StaffCreate):
    """
    Add a new staff member to Arkham Asylum.
    """
    # Generate new ID
    new_id = max(staff["id"] for staff in staff_db) + 1 if staff_db else 1
    
    # Create new staff record
    staff_dict = staff.dict()
    staff_dict["id"] = new_id
    staff_dict["hire_date"] = date.today().isoformat()
    
    staff_db.append(staff_dict)
    
    return staff_dict


@app.put("/staff/{staff_id}", response_model=StaffResponse)
async def update_staff(
    staff_id: int = Path(..., ge=1, description="The ID of the staff member to update"),
    staff_data: StaffUpdate = Body(...)
):
    """
    Update a staff member's information.
    """
    # Find the staff member
    for i, staff in enumerate(staff_db):
        if staff["id"] == staff_id:
            # Extract only the set fields (exclude unset fields)
            update_data = staff_data.dict(exclude_unset=True)
            
            # Update the staff data
            staff_db[i].update(update_data)
            return staff_db[i]
    
    raise HTTPException(status_code=404, detail=f"Staff member with ID {staff_id} not found")


# === Treatment endpoints ===
@app.get("/treatments/", response_model=List[TreatmentResponse])
async def list_treatments():
    """
    List all available treatments.
    """
    return treatments_db


@app.get("/treatments/{treatment_id}", response_model=TreatmentResponse)
async def get_treatment(treatment_id: int = Path(..., ge=1, description="The ID of the treatment to retrieve")):
    """
    Get a specific treatment by ID.
    """
    for treatment in treatments_db:
        if treatment["id"] == treatment_id:
            return treatment
    
    raise HTTPException(status_code=404, detail=f"Treatment with ID {treatment_id} not found")


@app.post("/treatments/", response_model=TreatmentResponse, status_code=status.HTTP_201_CREATED)
async def create_treatment(treatment: TreatmentCreate):
    """
    Create a new treatment program.
    """
    # Generate new ID
    new_id = max(treatment["id"] for treatment in treatments_db) + 1 if treatments_db else 1
    
    # Create new treatment record
    treatment_dict = treatment.dict()
    treatment_dict["id"] = new_id
    
    treatments_db.append(treatment_dict)
    
    return treatment_dict


@app.post("/inmates/{inmate_id}/treatments", response_model=TreatmentRecord, status_code=status.HTTP_201_CREATED)
async def assign_treatment(
    inmate_id: int = Path(..., ge=1, description="The ID of the inmate"),
    treatment_record: TreatmentRecord = Body(...)
):
    """
    Assign a treatment to an inmate.
    """
    # Verify the inmate exists
    inmate = None
    for i in inmates_db:
        if i["id"] == inmate_id:
            inmate = i
            break
    
    if not inmate:
        raise HTTPException(status_code=404, detail=f"Inmate with ID {inmate_id} not found")
    
    # Verify the treatment exists
    treatment = None
    for t in treatments_db:
        if t["id"] == treatment_record.treatment_id:
            treatment = t
            break
    
    if not treatment:
        raise HTTPException(status_code=404, detail=f"Treatment with ID {treatment_record.treatment_id} not found")
    
    # Create new treatment record
    record_dict = treatment_record.dict()
    record_dict["id"] = max(record["id"] for record in treatment_records_db) + 1 if treatment_records_db else 1
    record_dict["inmate_id"] = inmate_id  # Ensure the inmate ID matches the path parameter
    
    treatment_records_db.append(record_dict)
    
    return record_dict


# === Incident endpoints ===
@app.get("/incidents/", response_model=List[IncidentResponse])
async def list_incidents(
    inmate_id: Optional[int] = Query(None, description="Filter by inmate ID"),
    min_severity: Optional[int] = Query(None, ge=1, le=10, description="Minimum severity level"),
    after_date: Optional[date] = Query(None, description="Filter incidents after this date")
):
    """
    List all recorded incidents with optional filtering.
    """
    results = incidents_db.copy()
    
    # Apply filters
    if inmate_id is not None:
        results = [i for i in results if i["inmate_id"] == inmate_id]
    
    if min_severity is not None:
        results = [i for i in results if i["severity"] >= min_severity]
    
    if after_date is not None:
        results = [i for i in results if date.fromisoformat(i["date"]) >= after_date]
    
    return results


@app.post("/incidents/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(incident: IncidentCreate):
    """
    Record a new incident.
    """
    # Verify the inmate exists
    inmate = None
    for i in inmates_db:
        if i["id"] == incident.inmate_id:
            inmate = i
            break
    
    if not inmate:
        raise HTTPException(status_code=404, detail=f"Inmate with ID {incident.inmate_id} not found")
    
    # Verify all staff members exist
    for staff_id in incident.staff_involved:
        if not any(s["id"] == staff_id for s in staff_db):
            raise HTTPException(status_code=404, detail=f"Staff member with ID {staff_id} not found")
    
    # Generate new ID
    new_id = max(incident["id"] for incident in incidents_db) + 1 if incidents_db else 1
    
    # Create new incident record
    incident_dict = incident.dict()
    incident_dict["id"] = new_id
    incident_dict["date"] = incident.date.isoformat()
    
    incidents_db.append(incident_dict)
    
    return incident_dict


# === Knightfall Protocol endpoints ===
@app.get("/inmates/{inmate_id}/with-treatments", response_model=InmateWithTreatments)
async def get_inmate_with_treatments(
    inmate_id: int = Path(..., ge=1, description="The ID of the inmate to retrieve")
):
    """
    Get detailed inmate record with treatment history.
    """
    # Find the inmate
    inmate = None
    for i in inmates_db:
        if i["id"] == inmate_id:
            inmate = i
            break
    
    if not inmate:
        raise HTTPException(status_code=404, detail=f"Inmate with ID {inmate_id} not found")
    
    # Get treatment records for this inmate
    records = [record for record in treatment_records_db if record["inmate_id"] == inmate_id]
    
    # Create response with nested treatment records
    result = inmate.copy()
    result["treatment_records"] = records
    
    return result


@app.get("/inmates/{inmate_id}/case-file", response_model=ResponseBase[CaseFile])
async def get_inmate_case_file(
    inmate_id: int = Path(..., ge=1, description="The ID of the inmate to retrieve"),
    access_level: int = Query(5, ge=1, le=10, description="Staff access level (1-10)")
):
    """
    Get comprehensive case file for an inmate (requires high access level).
    """
    # Check access level
    if access_level < 8:
        return {
            "success": False,
            "message": "Insufficient access level",
            "errors": ["Access to case files requires level 8 clearance"]
        }
    
    # Find the inmate
    inmate = None
    for i in inmates_db:
        if i["id"] == inmate_id:
            inmate = i
            break
    
    if not inmate:
        raise HTTPException(status_code=404, detail=f"Inmate with ID {inmate_id} not found")
    
    # Get treatment records for this inmate
    treatment_records = [record for record in treatment_records_db if record["inmate_id"] == inmate_id]
    
    # Get incidents for this inmate
    inmate_incidents = [incident for incident in incidents_db if incident["inmate_id"] == inmate_id]
    
    # Create a mock location
    location = {
        "building": "Main Asylum",
        "wing": f"{inmate['cell_block']} Wing",
        "cell_number": f"{inmate['cell_block']}-{inmate_id}"
    }
    
    # Create case file
    case_file = {
        "inmate": inmate,
        "psychological_profile": f"Subject exhibits signs of {', '.join(inmate['disorders'])}. Requires continuous monitoring.",
        "threat_assessment": f"Danger level {inmate['danger_level']}/10. Specific protocols must be followed.",
        "escape_attempts": len([i for i in inmate_incidents if i["incident_type"] == "Escape Attempt"]),
        "known_associates": ["Joker", "Penguin"] if inmate_id == 1 else ["Two-Face", "Scarecrow"],  # Mock data
        "treatment_history": treatment_records,
        "incidents": inmate_incidents,
        "location": location
    }
    
    return {
        "success": True,
        "message": "Case file retrieved successfully",
        "data": case_file
    }


@app.get("/stats", response_model=Dict[str, Any])
async def get_asylum_stats():
    """
    Get statistics about Arkham Asylum.
    """
    active_inmates = len([i for i in inmates_db if i["is_active"]])
    
    # Count inmates by cell block
    inmates_by_block = {}
    for block in CellBlock:
        inmates_by_block[block.value] = len([i for i in inmates_db if i["cell_block"] == block.value])
    
    # Calculate average danger level
    avg_danger = sum(i["danger_level"] for i in inmates_db) / len(inmates_db) if inmates_db else 0
    
    # Count incidents by severity
    high_severity_incidents = len([i for i in incidents_db if i["severity"] >= 7])
    med_severity_incidents = len([i for i in incidents_db if 4 <= i["severity"] <= 6])
    low_severity_incidents = len([i for i in incidents_db if i["severity"] <= 3])
    
    return {
        "inmate_count": {
            "total": len(inmates_db),
            "active": active_inmates,
            "by_cell_block": inmates_by_block
        },
        "staff_count": len(staff_db),
        "avg_danger_level": round(avg_danger, 1),
        "incident_stats": {
            "total": len(incidents_db),
            "high_severity": high_severity_incidents,
            "medium_severity": med_severity_incidents,
            "low_severity": low_severity_incidents
        },
        "treatment_stats": {
            "total_treatments": len(treatments_db),
            "active_treatment_records": len([r for r in treatment_records_db if r["date_completed"] is None])
        }
    }


# For running the application directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
