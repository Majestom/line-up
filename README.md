# User Data Application

A full-stack application demonstrating API consumption, data reformatting, and user interface development. Built with Python FastAPI backend and React TypeScript frontend.

## Project Overview

This application consists of:

- **Backend**: Python FastAPI service that proxies requests to the [reqres.in](https://reqres.in) API
- **Frontend**: React TypeScript application with routing that displays user data
- **Docker**: Containerisation for easy deployment

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React App     │───▶│   FastAPI        │───▶│   reqres.in     │
│   (Frontend)    │    │   (Backend)      │    │   API           │
│   Port 5173     │    │   Port 8000      │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

The backend fetches data from reqres.in and reformats it to expose only user information. If the external API is unavailable, it provides helpful error messages to guide users. The frontend provides a clean interface to view user profiles with URL-based navigation.

## Features

- **URL-based routing**: Navigate to `/user/1` through `/user/12` to view different users
- **Interactive user switching**: Change user ID via input field
- **Responsive design**: Works on desktop and mobile devices
- **Error handling**: Graceful error messages for missing users or API failures
- **Type safety**: Full TypeScript implementation
- **Docker support**: Easy containerisation and deployment

## Technology Stack

### Backend

- **FastAPI**: Modern Python web framework
- **httpx**: Async HTTP client for external API calls
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the application

### Frontend

- **React**: Component-based UI framework
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and development server (requires Node.js 20.19+)
- **React Router**: Client-side routing

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Centralised configuration management
│   ├── models.py            # Pydantic data models
│   ├── api_client.py        # External API client
│   ├── middleware.py        # Request handling and logging
│   ├── health.py            # Health check endpoints
│   ├── users.py             # User data endpoints
│   ├── tests/               # Test suite
│   │   ├── test_api.py      # Integration tests
│   │   └── test_api_client.py # Unit tests
│   ├── requirements.txt     # Python dependencies
│   ├── pytest.ini          # Test configuration
│   └── Dockerfile          # Backend container config
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   ├── types/         # TypeScript type definitions
│   │   ├── App.tsx        # Main application component
│   │   └── main.tsx       # Application entry point
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend container config
├── .env.example           # Environment configuration template
├── .gitignore             # Git ignore rules
├── docker-compose.yml     # Multi-container setup
└── README.md              # This file
```

## Getting Started

### Prerequisites

- **Node.js** 20.19+ (for frontend development)
- **Python** 3.11+ (for backend development)
- **Docker** & **Docker Compose** (for containerised deployment)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd line-up
   ```

2. **Configure environment variables**

   ```bash
   # Copy the centralised environment file
   cp .env.example .env

   # The .env file contains all configuration for both frontend and backend
   # For development, the default values should work as-is
   # For production, edit .env and update the values as needed
   ```

3. **Start the application**

   ```bash
   docker compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory**

   ```bash
   cd backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   # Use the centralised .env file from project root
   # If running locally, the backend will read environment variables from the shell
   # Make sure you've set up the root .env file as described in the Docker setup above
   ```

5. **Run the backend server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Frontend Setup

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

## API Endpoints

### Backend API

- `GET /` - Root endpoint
- `GET /health` - Health check with dependency monitoring
- `GET /user/{user_id}` - Fetch user data by ID (1-12)
- `GET /docs` - Interactive API documentation

### Example Response

```json
{
  "data": {
    "id": 1,
    "email": "george.bluth@reqres.in",
    "first_name": "George",
    "last_name": "Bluth",
    "avatar": "https://reqres.in/img/faces/1-image.jpg"
  }
}
```

## Usage

1. **Home Page**: Visit http://localhost:5173 to see the application overview
2. **View Users**: Click on sample user buttons or navigate to `/user/{id}`
3. **Switch Users**: Use the input field on the user page to change between users
4. **Direct Navigation**: Access users directly via URL (e.g., `/user/5`)

## Security Best Practices

This project demonstrates proper security practices for handling API keys and environment variables:

### Environment Variables

- **Never commit `.env` files** to version control
- **Use `.env.example`** files to document required environment variables
- **Store production secrets** in secure environment variable stores (AWS Secrets Manager, Azure Key Vault, etc.)
- **Use different keys** for different environments (dev, staging, production)

### API Key Management

- **Principle of least privilege**: Use keys with minimal required permissions
- **Rotation**: Regularly rotate API keys in production
- **Monitoring**: Monitor API key usage for suspicious activity
- **Fallback handling**: Graceful degradation when API keys are invalid or missing

### Docker Security

- **Environment variable injection**: Use `${VARIABLE:-default}` syntax in docker-compose.yml
- **No secrets in images**: Keep secrets out of Docker images and layers
- **Runtime configuration**: Pass secrets at container runtime, not build time

## Development Notes

### Backend Decisions

- **FastAPI**: Chosen for automatic API documentation, type hints, and async support
- **httpx**: Used for async HTTP requests to external APIs
- **CORS middleware**: Configured to allow frontend connections
- **Error handling**: Comprehensive error responses for different failure scenarios

### Frontend Decisions

- **React Router**: Enables URL-based navigation as required
- **TypeScript**: Ensures type safety and better development experience
- **Component structure**: Separation of concerns with dedicated components and pages
- **CSS**: Custom styles for clean, responsive design

### Architecture Decisions

- **Proxy pattern**: Backend acts as a proxy to reqres.in, allowing data transformation
- **RESTful design**: Clean API endpoints following REST conventions
- **Docker support**: Both services containerised for easy deployment
- **Error boundaries**: Graceful error handling in the UI

## Testing

The backend includes a comprehensive test suite following best practices for FastAPI applications.

### Backend Testing

**Run the complete test suite:**

```bash
# Using Docker (recommended)
docker compose run --rm backend pytest tests/ -v

# Or locally (requires pytest installation)
cd backend
pytest tests/ -v
```

**Test Coverage:**

- **Integration tests** (`test_api.py`): Test all API endpoints with real FastAPI TestClient

  - Health endpoint functionality and structure
  - User endpoints with valid/invalid IDs
  - Error handling (404, 422 validation errors)
  - Request ID headers and CORS configuration
  - Root endpoint functionality

- **Unit tests** (`test_api_client.py`): Test core business logic
  - API client header configuration
  - Client initialisation and settings

**Manual API Testing:**

```bash
# Test user endpoint
curl http://localhost:8000/user/1

# Test health endpoint
curl http://localhost:8000/health

# Test root endpoint
curl http://localhost:8000/
```

**Expected Test Results:** All tests should pass (12 tests total: 9 integration, 3 unit)

### Frontend Testing

Manual testing approach:

- Navigate to different user URLs (`/user/1` through `/user/12`)
- Test input field functionality for user switching
- Verify responsive design on different screen sizes
- Test error handling with invalid user IDs

## Deployment

The application is designed to be easily deployable using Docker Compose. For production:

1. **Modify environment variables** as needed
2. **Update CORS settings** in the backend for production domains
3. **Configure reverse proxy** if needed
4. **Set up monitoring** and logging as required

## Future Enhancements

- Add user search functionality
- Implement pagination for larger user sets
- Add user data caching
- Include unit and integration tests
- Add loading skeletons for better UX
- Implement dark/light theme toggle

## License

This project is for demonstration purposes.
