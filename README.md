# Flask REST API

A simple REST API built with Flask and SQLite. Uses Flasgger for API documentation.

## Live Demo

**API is live at:** [https://indus-part1.onrender.com](https://indus-part1.onrender.com)

**API Documentation:** [https://indus-part1.onrender.com/apidocs](https://indus-part1.onrender.com/apidocs)

## Requirements

- Python 3.8+
- uv (Python package manager)

## Setup

### Install uv

```sh
pip install uv
```

### Create virtual environment

```sh
uv venv .venv
```

### Activate virtual environment

**Windows:**
```sh
.venv\Scripts\activate
```

**macOS/Linux:**
```sh
source .venv/bin/activate
```

### Install dependencies

```sh
uv pip install flask flasgger
```

## Run the app

```sh
python app.py
```

The database will be created automatically on first run.

## API Documentation

Visit [http://localhost:5000/apidocs](http://localhost:5000/apidocs) for Swagger UI.

## Authentication

All endpoints need an API key in the header:

```
x-api-key: my_secure_api_key
```

## Endpoints

- `POST /records` - Add a new record
- `GET /records` - List all records (can filter by status)
- `PUT /records/<record_id>` - Update a record
- `DELETE /records/<record_id>` - Delete a record

See `/apidocs` for full details.

## Testing the API

### Using the Live Demo

1. Visit [https://indus-part1.onrender.com/apidocs](https://indus-part1.onrender.com/apidocs)
2. Click "Authorize" and enter: `my_secure_api_key`
3. Test the endpoints using the Swagger UI

### Using curl

```bash
# Add a record
curl -X POST "https://indus-part1.onrender.com/records" \
  -H "x-api-key: my_secure_api_key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Record", "status": "active"}'

# Get all records
curl -X GET "https://indus-part1.onrender.com/records" \
  -H "x-api-key: my_secure_api_key"
```