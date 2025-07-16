# Flask REST API

A simple REST API built with Flask and SQLite. Uses Flasgger for API documentation.

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