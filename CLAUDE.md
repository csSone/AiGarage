# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AiGarage is an experimental project exploring vLLM and SGLang for running large language models and building intelligent Agent systems. The project uses a microservices architecture with Go backend, Python model server, and Vue 3 frontend.

## Architecture

The project consists of three main components:

1. **Backend** (`backend/`): Go service using Gin framework
   - Entry point: `main.go`
   - Listens on port 8080 by default
   - Managed by `start.sh` script with PID tracking and auto-restart

2. **Model Server** (`model_server/`): Python vLLM service
   - Entry point: `server.py`
   - Provides OpenAI-compatible API endpoints (`/v1/chat/completions`)
   - Requires `MODEL_PATH` environment variable
   - Default port: 8000 (configurable via `PORT` env var)

3. **Frontend** (`web/`): Vue 3 + TypeScript + Vite
   - Development server runs on port 7016
   - Uses Element Plus UI library with auto-import
   - Vue Router for navigation

## Common Commands

### Backend (Go)
```bash
# Build and run backend (use start.sh for production with supervision)
cd backend
go build -o server main.go
./server

# Or use the start script which handles PID tracking and auto-restart
./start.sh
```

### Model Server (Python)
```bash
cd model_server
export MODEL_PATH=/path/to/model
export PORT=8000  # optional, defaults to 8000
python -m model_server.server
```

### Frontend (Vue)
```bash
cd web
npm install
npm run dev      # Development server on :7016
npm run build    # Production build
npm run preview  # Preview production build
```

### Docker Deployment
```bash
cd docker
docker-compose up -d
```

## Environment Configuration

Copy `.env.example` to `.env` and configure:
- `MODEL_PATH`: Required path to the LLM model files
- `PORT`: Model server port (default: 8000)
- `BACKEND_PATH`: Path to backend directory (used by start.sh)

## Key Dependencies

- **Backend**: Gin web framework (Go 1.23.4)
- **Model Server**: vllm==0.8.1, uvicorn, fastapi
- **Frontend**: Vue 3, Element Plus, Vue Router, Vite

## Project Structure Notes

- `lib/`: Shared Go library (linked via go.mod replace directive)
- `nginx/`: Reverse proxy configuration for production
- `log/`: Application logs (backend.log, build.log, start.log)
- The `start.sh` script manages the backend process lifecycle with PID tracking
