#!/usr/bin/env python3
"""
Arkham Asylum Management API
----------------------------
Your mission: Create a comprehensive API for Arkham Asylum's records
using FastAPI with Pydantic models and request bodies.
"""
from fastapi import FastAPI, Path, Query, HTTPException, Body, status
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import date, datetime
import uvicorn

# Initialize our Arkham API
app = FastAPI(
    title="Arkham Asylum API",
    description="Management system for Arkham Asylum's inmate records",
    version="1.0.0"
)

# Sample database (in a real app, this would be a database)
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

# TODO: Define a CellBlock enum with values A, B, C, D
# class CellBlock(...):
#     ...

# TODO: Define a base Person model with common fields
# class PersonBase(...):
#     ...

# TODO: Define Inmate model (request body)
# class InmateCreate(...):
#     ...

# TODO: Define Inmate response model
# class InmateResponse(...):
#     ...

# TODO: Define Staff model 
# class StaffCreate(...):
#     ...

# TODO: Define Treatment model
# class Treatment(...):
#     ...

# TODO: Define Incident model
# class Incident(...):
#     ...

# TODO: Define a nested TreatmentRecord model
# class TreatmentRecord(...):
#     ...

# TODO: Define enhanced Inmate model with treatment records
# class InmateWithTreatments(...):
#     ...

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

# TODO: Implement endpoint to list all inmates
# @app.get(...)
# async def list_inmates(...):
#     """List all inmates."""
#     ...

# TODO: Implement endpoint to get a specific inmate
# @app.get(...)
# async def get_inmate(...):
#     """Get a specific inmate by ID."""
#     ...

# TODO: Implement endpoint to create a new inmate with request body
# @app.post(...)
# async def create_inmate(...):
#     """Add a new inmate to Arkham Asylum."""
#     ...

# TODO: Implement endpoint to update an inmate
# @app.put(...)
# async def update_inmate(...):
#     """Update an inmate's information."""
#     ...

# === Staff endpoints ===

# TODO: Implement endpoint to list all staff members
# @app.get(...)
# async def list_staff(...):
#     """List all staff members."""
#     ...

# TODO: Implement endpoint to get a specific staff member
# @app.get(...)
# async def get_staff_member(...):
#     """Get a specific staff member by ID."""
#     ...

# === Treatment endpoints ===

# TODO: Implement endpoint to list all treatments
# @app.get(...)
# async def list_treatments(...):
#     """List all available treatments."""
#     ...

# TODO: Implement endpoint to assign a treatment to an inmate
# @app.post(...)
# async def assign_treatment(...):
#     """Assign a treatment to an inmate."""
#     ...

# === Incident endpoints ===

# TODO: Implement endpoint to list all incidents
# @app.get(...)
# async def list_incidents(...):
#     """List all recorded incidents."""
#     ...

# TODO: Implement endpoint to create a new incident
# @app.post(...)
# async def create_incident(...):
#     """Record a new incident."""
#     ...

# === Advanced Knightfall Protocol endpoints ===

# TODO: Implement endpoint to get an inmate with their treatment history
# @app.get(...)
# async def get_inmate_with_treatments(...):
#     """Get detailed inmate record with treatment history."""
#     ...

# For running the application directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
