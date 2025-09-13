# User Data Application

A full-stack application demonstrating API consumption, data reformatting, and user interface development. Built with Python FastAPI backend and React TypeScript frontend.

## Project Overview

This application consists of:
- **Backend**: Python FastAPI service that proxies requests to the [reqres.in](https://reqres.in) API
- **Frontend**: React TypeScript application with routing that displays user data
- **Docker**: Containerization for easy deployment

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
- **Docker support**: Easy containerization and deployment

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
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container config
│   └── .env               # Environment variables
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
├── docker-compose.yml     # Multi-container setup
└── README.md              # This file
```

## Getting Started

### Prerequisites

- **Node.js** 20.19+ (for frontend development)
- **Python** 3.11+ (for backend development)
- **Docker** & **Docker Compose** (for containerized deployment)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd line-up
   ```

2. **Start the application**
   ```bash
   docker compose up --build
   ```

3. **Access the application**
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

4. **Run the backend server**
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

- `GET /` - Health check endpoint
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
- **Docker support**: Both services containerized for easy deployment
- **Error boundaries**: Graceful error handling in the UI

## Testing

### Backend Testing
```bash
cd backend
# Test the API endpoint
curl http://localhost:8000/user/1
```

### Frontend Testing
- Navigate to different user URLs
- Test input field functionality
- Verify responsive design on different screen sizes

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