# Gotham FastAPI Learning Path

A comprehensive Batman-themed curriculum to learn Python and FastAPI through engaging, practical lessons.

## Project Objective

This project provides a structured learning path to master Python and FastAPI through the lens of Batman's world. By framing programming concepts in the familiar context of Gotham City, complex technical ideas become more approachable and memorable.

The curriculum is designed for progressive learning - starting with Python fundamentals, building to FastAPI basics, advancing to more complex API concepts, and culminating in deployment and integration. Each lesson includes theory with Batman-themed examples, practical projects, additional challenges, and complete solution code.

## Curriculum Structure

### Phase 1: Python Fundamentals with FastAPI Context
1. **The Dark Knight Begins**: Python basics, environment setup
2. **Gadget Development**: Variables, data types, and functions
3. **Bat-Family Coordination**: Control structures and error handling
4. **Becoming the Batman**: Object-oriented programming in Python

### Phase 2: FastAPI Fundamentals
5. **Batcomputer Database**: FastAPI basics and first API
6. **Power Classification**: Path parameters and query parameters
7. **Arkham Records**: Request bodies and data models (Pydantic)
8. **Oracle's Interface**: API documentation with Swagger UI (/docs)

### Phase 3: Advanced FastAPI Concepts
9. **GCPD Case Files**: Database integration (SQL and NoSQL)
10. **Wayne Manor Security**: Authentication and authorization
11. **Bat-Signal Protocols**: Background tasks and scheduling
12. **Bat-Gadget Integration**: File operations and handling

### Phase 4: Deployment and Integration
13. **Batmobile Engineering**: Containerization with Docker
14. **The Watchtower**: Kubernetes deployment
15. **Alfred's Intelligence**: OpenAI API integration
16. **Gotham's Protector**: Building a complete vigilante management application

## How to Use This Curriculum

Each lesson follows a consistent structure:

1. **README.md** - Detailed explanations of concepts with Batman-themed examples
2. **starter_code.py** - Scaffolding code with TODOs to complete
3. **helper_guide.md** - "Bruce Wayne's Journal" with implementation hints
4. **solution.py** - Complete working code with comments

### Suggested Learning Approach

1. Read the lesson's README.md to understand the concepts
2. Try implementing the project using starter_code.py
3. If you get stuck, consult helper_guide.md for guidance
4. Compare your solution with solution.py after completing your implementation
5. Take on the "Knightfall Protocol" challenge for more advanced practice

## Running the Code

Most lessons can be run directly with Python:

```bash
python lesson_x/solution.py
```

For FastAPI projects (Lesson 5 and beyond), use Uvicorn:

```bash
cd lesson_x
uvicorn solution:app --reload
```

Then visit http://127.0.0.1:8000/docs to see and test your API using Swagger UI.

## Prerequisites

- Python 3.8 or higher
- Understanding of basic programming concepts
- For later lessons: FastAPI and Uvicorn installed (`pip install fastapi uvicorn`)

Remember, in the words of Batman: "It's not who I am underneath, but what I do that defines me." Happy coding!
