# Flask Task Management API with SQLite

An intermediate-level REST API built with Flask and SQLite, featuring a complete CRUD system with database relationships, foreign keys, and transaction handling.

## Features

- **Full CRUD Operations**: Create, Read, Update, and Delete tasks
- **SQLite Database**: Persistent data storage with proper schema design
- **Foreign Key Relationships**: Categories linked to tasks with referential integrity
- **Transaction Handling**: Atomic operations with COMMIT/ROLLBACK
- **Auto-Category Creation**: Categories are automatically created when adding tasks
- **Data Validation**: CHECK constraints for status and priority fields
- **Professional Error Handling**: Proper HTTP status codes and error messages

## Technologies Used

- Python 3
- Flask (Web Framework)
- SQLite3 (Database)
- RESTful API design principles

## Database Schema

### Categories Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TEXT
)
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT NOT NULL DEFAULT 'Medium',
    due_date TEXT,
    status TEXT NOT NULL DEFAULT 'Pending',
    created_at TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    CHECK(status IN('Pending', 'In Progress', 'Completed')),
    CHECK(priority IN('Low', 'Medium', 'High'))
)
```

## API Endpoints

### Get All Tasks
```
GET /api/tasks
```
**Response:** Array of all tasks with category information

### Get Single Task
```
GET /api/tasks/<id>
```
**Response:** Single task object or 404 error

### Create New Task
```
POST /api/tasks
Content-Type: application/json

{
  "title": "Task name",
  "description": "Task description",
  "priority": "High",
  "due_date": "2025-12-20",
  "category": "Work"
}
```
**Response:** 201 Created with success message

### Update Task
```
PUT /api/tasks/<id>
Content-Type: application/json

{
  "status": "Completed",
  "priority": "Low"
}
```
**Response:** 200 OK with success message or 404 if not found

### Delete Task
```
DELETE /api/tasks/<id>
```
**Response:** 200 OK with success message or 404 if not found

## Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/jandaghi14/intermediate-flask-sqlite-task-api.git
cd intermediate-flask-sqlite-task-api
```

2. **Install Flask:**
```bash
pip install flask
```

3. **Run the application:**
```bash
python app.py
```

4. **Server runs on:** `http://127.0.0.1:5000`

## Testing with curl

**Create a task:**
```bash
curl -X POST http://127.0.0.1:5000/api/tasks -H "Content-Type: application/json" -d "{\"title\": \"Learn Flask\", \"description\": \"Build REST APIs\", \"priority\": \"High\", \"due_date\": \"2025-12-20\", \"category\": \"Education\"}"
```

**Get all tasks:**
```bash
curl http://127.0.0.1:5000/api/tasks
```

**Get single task:**
```bash
curl http://127.0.0.1:5000/api/tasks/1
```

**Update task status:**
```bash
curl -X PUT http://127.0.0.1:5000/api/tasks/1 -H "Content-Type: application/json" -d "{\"status\": \"Completed\"}"
```

**Delete task:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/tasks/2
```

## Advanced Features

### Foreign Key Enforcement
- PRAGMA foreign_keys = ON ensures referential integrity
- Tasks cannot exist without a valid category
- Categories are protected from deletion if tasks reference them

### Transaction Safety
- All database operations use proper commit/rollback patterns
- Connection pooling is handled correctly
- No orphaned connections or memory leaks

### Dynamic SQL
- UPDATE operations only modify specified fields
- NULL values are handled correctly
- SQL injection is prevented with parameterized queries

## Project Structure
```
intermediate-flask-sqlite-task-api/
│
├── app.py              # Flask application and API routes
├── database.py         # Database operations and schema
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## What I Learned

- Building RESTful APIs with Flask
- SQLite database design with foreign keys
- Transaction management and data integrity
- HTTP methods and status codes
- API testing with curl
- Professional error handling
- Modular code architecture
- Git workflow and GitHub collaboration

## Future Improvements

- Add user authentication (JWT tokens)
- Implement pagination for large datasets
- Add data validation middleware
- Create API documentation (Swagger/OpenAPI)
- Deploy to production (Heroku/PythonAnywhere)
- Add unit tests (pytest)
- Implement rate limiting
- Add category management endpoints

## License

This project is open source and available for educational purposes.

## Author

Built as part of a Python learning journey - Day 48 of 225 days to job-ready.