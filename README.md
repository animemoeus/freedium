# Freedium - FastAPI with Template Rendering

A modern FastAPI application with Jinja2 template rendering, featuring a clean modular structure and both API and web interfaces.

## Features

- **FastAPI Backend**: Modern, fast web framework for building APIs
- **Jinja2 Templates**: Server-side template rendering for web pages
- **Modular Structure**: Clean separation of concerns with organized code
- **Static File Serving**: CSS, JavaScript, and image assets
- **Bootstrap UI**: Responsive web interface
- **Form Handling**: HTML form processing with validation
- **API Endpoints**: RESTful API alongside web interface

## Project Structure

```
freedium/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app configuration
│   ├── config.py            # Application settings
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── api.py           # API endpoints
│   │   └── web.py           # Web page routes
│   └── services/
│       ├── __init__.py
│       └── url_service.py   # Business logic
├── templates/
│   ├── base.html            # Base template with layout
│   ├── index.html           # Home page
│   ├── about.html           # About page
│   └── result.html          # Result page
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   └── js/
│       └── main.js          # JavaScript functionality
├── tests/
│   └── test_url_service.py  # Unit tests
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Project configuration
└── .gitignore              # Git ignore patterns
```

## Installation

1. Create a virtual environment:
```bash
python -m venv .env
source .env/bin/activate  # On Windows: .env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
python main.py
```

The application will be available at:
- Web interface: http://localhost:8000
- API documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Home page (web interface)
- `GET /about` - About page (web interface)
- `POST /validate` - URL validation form handler
- `GET /api/` - API root endpoint
- `GET /api/validate-url?url=<url>` - URL validation API

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black app/ tests/
```

### Type Checking
```bash
mypy app/
```

## Environment Variables

- `DEBUG`: Enable debug mode (default: False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

## License

MIT License