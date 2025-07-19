# Notes Backend API Documentation

This document provides a comprehensive overview of the RESTful API exposed by the Notes Backend container, which is built with FastAPI. The API allows users to create, read, update, and delete notes, with file-based JSON persistence for storage. No authentication is currently implemented; all endpoints are public.

## API Overview

- **Base URL:** `/` (root of the FastAPI app)
- **Version:** 1.0.0
- **Framework:** FastAPI
- **Authentication:** None (all endpoints are public)
- **Content-Type:** `application/json`

---

## Endpoints

### 1. Health Check

**GET /**

- **Summary:** Simple health check endpoint.
- **Returns:** `{ "message": "Healthy" }`
- **Status Codes:**
  - 200 OK – if service is running

**Example Request:**  
`GET /`

**Example Response:**
```json
{
  "message": "Healthy"
}
```

---

### 2. List Notes

**GET /notes**

- **Summary:** List all notes.
- **Returns:** An array of all stored notes.
- **Status Codes:**
  - 200 OK – successful retrieval

**Example Request:**  
`GET /notes`

**Example Response:**
```json
[
  {
    "id": 1,
    "title": "Example Note",
    "content": "This is the content of the note.",
    "created_at": "2024-06-22T15:10:00.000000"
  }
]
```

---

### 3. Get Note by ID

**GET /notes/{note_id}**

- **Summary:** Retrieve a single note by its identifier.
- **Parameters:**
  - `note_id` (int, required): The ID of the note to retrieve.
- **Returns:** The note with the specified ID.
- **Status Codes:**
  - 200 OK – note found and returned
  - 404 Not Found – note with that ID does not exist

**Example Request:**  
`GET /notes/1`

**Example Success Response:**
```json
{
  "id": 1,
  "title": "Example Note",
  "content": "This is the content of the note.",
  "created_at": "2024-06-22T15:10:00.000000"
}
```
**Example Error Response (404):**
```json
{
  "detail": "Note not found"
}
```

---

### 4. Create a New Note

**POST /notes**

- **Summary:** Create a new note.
- **Request Body:** JSON object matching the `NoteCreate` model.
- **Returns:** The newly created note (with assigned ID and timestamp).
- **Status Codes:**
  - 201 Created – note was successfully created
  - 422 Unprocessable Entity – validation error

#### Request Body Schema (`NoteCreate`)
| Field   | Type   | Required | Description          |
|---------|--------|----------|----------------------|
| title   | string | Yes      | Title of the note    |
| content | string | Yes      | Content of the note  |

**Example Request Payload:**
```json
{
  "title": "Project Thoughts",
  "content": "Let's brainstorm some project ideas!"
}
```

**Example Success Response (201):**
```json
{
  "id": 2,
  "title": "Project Thoughts",
  "content": "Let's brainstorm some project ideas!",
  "created_at": "2024-06-22T15:20:00.000000"
}
```

**Example Error Response (422, Validation):**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### 5. Update an Existing Note

**PUT /notes/{note_id}**

- **Summary:** Update a note by its ID.
- **Parameters:**
  - `note_id` (int, required): ID of the note to update.
- **Request Body:** JSON object matching the `NoteUpdate` model.
- **Returns:** The updated note.
- **Status Codes:**
  - 200 OK – update successful
  - 404 Not Found – note not found
  - 422 Unprocessable Entity – validation error

#### Request Body Schema (`NoteUpdate`)
| Field   | Type   | Required | Description          |
|---------|--------|----------|----------------------|
| title   | string | No       | Updated note title   |
| content | string | No       | Updated note content |

**Example Request Payload:**
```json
{
  "title": "Updated Note Title"
}
```

**Example Success Response:**
```json
{
  "id": 1,
  "title": "Updated Note Title",
  "content": "This is the content of the note.",
  "created_at": "2024-06-22T15:10:00.000000"
}
```

**Example Error Response (404):**
```json
{
  "detail": "Note not found"
}
```
**Example Error Response (422, Validation):**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "value is not a valid string",
      "type": "type_error.string"
    }
  ]
}
```

---

### 6. Delete a Note

**DELETE /notes/{note_id}**

- **Summary:** Delete a note by its ID.
- **Parameters:**
  - `note_id` (int, required): ID of the note to delete.
- **Returns:** No content.
- **Status Codes:**
  - 204 No Content – deletion successful
  - 404 Not Found – note not found
  - 422 Unprocessable Entity – invalid parameter

**Example Request:**  
`DELETE /notes/1`

**Example Success Response:**
HTTP status code: `204 No Content`  
_Response body is empty._

**Example Error Response (404):**
```json
{
  "detail": "Note not found"
}
```

---

## Data Models

### Note

Represents a note with its assigned metadata.

| Field      | Type    | Description                        |
|------------|---------|------------------------------------|
| id         | int     | Unique identifier for the note     |
| title      | string  | Title of the note                  |
| content    | string  | Content of the note                |
| created_at | string (datetime) | Timestamp of creation    |


### NoteCreate

The request body model for creating a note.

| Field   | Type   | Required | Description         |
|---------|--------|----------|---------------------|
| title   | string | Yes      | Title of the note   |
| content | string | Yes      | Content of the note |


### NoteUpdate

The request body for updating a note. All fields are optional and default to no change.

| Field   | Type   | Required | Description              |
|---------|--------|----------|--------------------------|
| title   | string | No       | Updated note title       |
| content | string | No       | Updated note content     |

---

## Status Codes

| Code | When                                                     |
|------|----------------------------------------------------------|
| 200  | Successful GET, PUT                                      |
| 201  | Note successfully created                                |
| 204  | Note successfully deleted                                |
| 404  | Note not found (GET, PUT, DELETE by id)                  |
| 422  | Validation error in input parameters or payloads         |

---

## Authentication

**There is no authentication or authorization required for any endpoints. The API is open.** 

If deploying this application in production, consider adding authentication to prevent unauthorized access or data loss.

---

## Example Usage (with `curl`)

- **Create a note:**
  ```
  curl -X POST "http://<host>/notes" \
    -H "Content-Type: application/json" \
    -d '{"title":"Test Note","content":"Some content"}'
  ```
- **Get all notes:**
  ```
  curl http://<host>/notes
  ```
- **Get a specific note:**
  ```
  curl http://<host>/notes/1
  ```
- **Update a note:**
  ```
  curl -X PUT "http://<host>/notes/1" \
    -H "Content-Type: application/json" \
    -d '{"title":"Updated Title"}'
  ```
- **Delete a note:**
  ```
  curl -X DELETE http://<host>/notes/1
  ```

---

## Additional Details

- All data is stored in a JSON file (`notes_data.json`) on the server; this is not intended for concurrent multi-user production use.
- `created_at` timestamps are in UTC and conform to ISO 8601 datetime strings.
- IDs are assigned incrementally and monotonically as notes are created.
- If a non-existent note_id is requested or deleted, the API returns a 404 error.

---

## OpenAPI Specification

An up-to-date OpenAPI specification is also available at `/openapi.json` (if running the server) and visually browsable via FastAPI docs at `/docs`.

---
