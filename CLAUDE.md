# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AiGarage is an experimental project exploring vLLM and SGLang for running large language models and building intelligent Agent systems. The project uses a microservices architecture with Go backend, Python model server (as an AI provider gateway), and Vue 3 frontend.

## Architecture

The project consists of three main components:

1. **Backend** (`backend/`): Go service using Gin framework
   - Entry point: `main.go`
   - Listens on port 8080 by default
   - Managed by `start.sh` script with PID tracking and auto-restart
   - Uses structured logging to `backend/app.log`

2. **Model Server** (`model_server/`): Python FastAPI service acting as an AI provider gateway
   - Entry point: `server.py` (run as module: `python -m model_server.server`)
   - Provides OpenAI-compatible `/v1/chat/completions` endpoint
   - Routes requests to multiple AI providers: OpenAI, Anthropic, Google, ZAI (智谱)
   - Default port: 8000 (configurable via `PORT` env var)
   - Python tooling configured in `pyproject.toml` (black, isort, mypy, pytest)
   - No local model loading required - uses external API providers

3. **Frontend** (`web/`): Vue 3 + TypeScript + Vite
   - Development server runs on port 7016
   - Uses Element Plus UI library with auto-import (configured in `vite.config.ts`)
   - Vue Router for navigation
   - Strict TypeScript enabled with additional checks

4. **Nginx** (`nginx/`): Reverse proxy
   - Single entry point on ports 80/443
   - Routes to backend, model-server, and frontend services
   - Configuration in `nginx/conf.d/default.conf`

5. **Docker Deployment** (`docker/`): Complete containerization
   - Base config: `docker-compose.yml`
   - Development override: `docker-compose.dev.yml` (adds volume mounts for hot reload)
   - Production override: `docker-compose.prod.yml` (resource limits, optimizations)
   - Environment files: `.env`, `.env.development`, `.env.production`

**Service Communication Flow:**
- Frontend (port 7016) → Nginx (port 80/443) → Backend (port 8080) → Model Server (port 8000) → External AI APIs
- All services connected via `aigarage-network` bridge network
- Health checks configured for all services with wget/curl

## Common Commands

### Backend (Go)
```bash
cd backend
# Build and run
go build -o server main.go
./server

# Or use the start script with PID tracking and auto-restart
cd /home/semon/workspace/AiGarage
./start.sh

# Code quality
go test -v -race ./...
go vet ./...
golangci-lint run --config=.golangci.yml
go fmt ./...
```

### Model Server (Python)
```bash
cd model_server
# Run (requires API keys in environment)
export OPENAI_API_KEY=sk-...  # or ANTHROPIC_API_KEY, GOOGLE_API_KEY, ZAI_API_KEY
export PORT=8000  # optional
python -m model_server.server

# Code quality
black .
isort .
mypy .
flake8 . --max-line-length=88
pytest
```

### Frontend (Vue)
```bash
cd web
npm install
npm run dev      # Development server on :7016
npm run build    # Production build (includes vue-tsc type checking)
npm run preview  # Preview production build

# Type checking
npx vue-tsc --noEmit
```

### Docker Deployment
```bash
cd docker
# Development (with hot reload)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

# Production (optimized)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# View logs
docker-compose logs -f [service-name]

# Stop services
docker-compose down
```

## Environment Configuration

### Local Development
Copy `.env.example` to `.env` and configure:
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `GOOGLE_API_KEY`: Google AI API key
- `ZAI_API_KEY`: 智谱 (ZAI) API key
- `PORT`: Model server port (default: 8000)
- `BACKEND_PATH`: Path to backend directory (used by start.sh, default: `backend`)

**Note:** The model server acts as a gateway to external AI providers. Local model deployment via vLLM is optional - set `MODEL_PATH` only if running local models.

### Docker Environment
For Docker deployment, configure environment in `docker/.env`:
- Same API keys as above
- `GIN_MODE=release` for production
- `NODE_ENV=development` or `production`
- `LOG_LEVEL=info` or `debug`

## Key Dependencies

- **Backend**: Gin web framework (Go 1.23.4)
- **Model Server**: vllm==0.8.1 (optional for local models), uvicorn, fastapi
- **Frontend**: Vue 3, Element Plus, Vue Router, Vite, TypeScript 5.9

## Project Structure Notes

- `lib/`: Shared Go library (linked via go.mod replace directive) - currently empty, reserved for future shared code
- `log/`: Application logs (backend.log, build.log, start.log)
- `scripts/`: Deployment scripts (dev, prod, frontend build)
- The `start.sh` script at project root manages all services with Docker Compose

## Development Standards and Guidelines

### 1. Frontend Development Rules (Vue 3 + TypeScript)

**MUST:**
- Use Composition API with `<script setup lang="ts">` syntax
- Define component props with `defineProps<T>()` and emits with `defineEmits<T>()`
- Use explicit type annotations for props, emits, and refs ( interfaces preferred)
- Enable strict mode in TypeScript (already configured in `tsconfig.app.json`)
- Use `unknown` instead of `any` for truly unknown types
- Keep components under 300 lines; split if larger
- Use `scoped` CSS for component-specific styles

**MUST NOT:**
- Use `any` type (except in migration code with TODO comments)
- Use Options API for new components
- Create deeply nested component hierarchies (>5 levels)

**SHOULD:**
- Use PascalCase for component names (e.g., `NavBar.vue`, `Home.vue`)
- Organize by feature: `web/src/components/` (reusable), `web/src/view/` (pages), `web/src/composables/` (shared logic)
- Use discriminated unions for complex state types
- Leverage TypeScript's type inference for obvious cases
- Create shared types in `web/src/types/` directory
- Use utility types (`Partial<T>`, `Pick<T>`, `Omit<T>`) to derive types

**EXAMPLE:**
```typescript
<script setup lang="ts">
interface Props {
  title: string
  count?: number
}

interface Emits {
  (e: 'update', value: number): void
  (e: 'delete', id: string): void
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
})

const emit = defineEmits<Emits>()

// Use ref with explicit type for complex objects
interface User {
  id: string
  name: string
}
const users = ref<User[]>([])

// Use computed for derived state
const totalCount = computed(() => users.value.length)
</script>
```

**State Management:**
- Use `ref<T>()` for primitives and reactive objects
- Use `reactive<T>()` for complex nested objects
- Maintain immutable update patterns: `state.value = [...state.value, newItem]`
- Use Pinia for global state when needed (currently not in dependencies)

### 2. Backend API Development Rules (Go + Gin)

**MUST:**
- Follow RESTful principles with plural nouns (`/api/users`, not `/api/user`)
- Return consistent JSON response structure
- Include appropriate HTTP status codes (200, 201, 204, 400, 401, 403, 404, 409, 422, 500)
- Support pagination for list endpoints with `page` and `page_size` query parameters
- Never expose sensitive information in error messages or logs
- Handle all errors explicitly with logging

**MUST NOT:**
- Use verbs in endpoint paths (e.g., `/getUsers`)
- Return nested resources beyond 3 levels
- Mix data formats (always return JSON)

**SHOULD:**
- Version APIs via URL path (`/api/v1/...`)
- Use kebab-case for query parameters
- Follow standard Go project layout: `handlers/`, `services/`, `models/`, `middleware/`, `config/`
- Write godoc comments for exported functions
- Keep functions under 50 lines

**STANDARD RESPONSE FORMAT:**
```go
type ApiResponse struct {
    Data    interface{} `json:"data"`
    Status  int         `json:"status"`
    Message string      `json:"message,omitempty"`
}

type PaginatedResponse struct {
    Data       interface{} `json:"data"`
    Pagination Pagination  `json:"pagination"`
    Status     int         `json:"status"`
}
```

**NAMING CONVENTIONS:**
- Filenames: `snake_case.go`
- Package names: lowercase, single word
- Exported: `PascalCase`
- Private: `camelCase`
- Interfaces: `PascalCase` ending with `-er` suffix

**EXAMPLE:**
```go
// package: handlers
// file: user_handler.go

type UserHandler struct {
    userService *services.UserService
}

func NewUserHandler(userService *services.UserService) *UserHandler {
    return &UserHandler{userService: userService}
}

func (h *UserHandler) GetByID(c *gin.Context) {
    id := c.Param("id")
    user, err := h.userService.FindByID(id)
    if err != nil {
        logger.Printf("Error finding user %s: %v", id, err)
        c.JSON(500, gin.H{
            "error": gin.H{"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"},
            "status": 500,
        })
        return
    }
    c.JSON(200, gin.H{"data": user, "status": 200})
}
```

### 3. Python Development Rules (FastAPI)

**MUST:**
- Use type hints for all function parameters and return values
- Define Pydantic models for all request/response bodies with validation
- Use async/await for I/O operations
- Return Pydantic models for responses
- Define OpenAPI documentation for all endpoints
- Use appropriate HTTP status codes

**MUST NOT:**
- Use bare `except:` clauses
- Mix `None` returns with typed returns without `Optional`

**SHOULD:**
- Use modern type hints (Python 3.9+ style: `list[str]` instead of `List[str]`)
- Organize routes using FastAPI Router
- Implement health check and metrics endpoints
- Use dependency injection for shared logic
- Configure CORS middleware for frontend

**EXAMPLE:**
```python
from pydantic import BaseModel, Field
from typing import Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., min_length=1, max_length=4096)

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: str
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)

async def generate_completion(request: ChatRequest) -> ChatResponse:
    """Generate chat completion using external AI provider."""
    pass
```

**Code Quality:**
- Format with `black` (line length: 88)
- Sort imports with `isort` (profile: black)
- Type check with `mypy` (configured in `pyproject.toml`)
- Lint with `flake8`

### 4. Docker and Container Standards

**MUST:**
- Use multi-stage builds for production images
- Run containers as non-root user
- Use specific version tags (not `latest`)
- Include health checks in all services
- Use `.dockerignore` files

**SHOULD:**
- Optimize layer caching (order commands by change frequency)
- Scan images for vulnerabilities
- Use custom bridge networks for service isolation

**Development vs Production:**
- Development: Use `docker-compose.dev.yml` with volume mounts for hot reload
- Production: Use `docker-compose.prod.yml` with resource limits and optimizations
- Environment-specific configs in `.env.development` and `.env.production`

### 5. Automation and Quality Assurance

**Pre-commit Hooks** (configured in `.pre-commit-config.yaml`):
- Frontend: ESLint with auto-fix for `.ts`, `.tsx`, `.vue` files
- Python: black, isort, flake8
- Go: golangci-lint, go-fmt
- General: JSON/YAML/TOML validation, end-of-file-fixer, trailing-whitespace

**CI/CD** (GitHub Actions):
- `.github/workflows/ci.yml`: Full CI pipeline on push/PR to main, develop, feature/* branches
- Includes: TypeScript build (vue-tsc), Go tests/vet/build, Python black/isort/flake8/mypy, Trivy security scan
- `.github/workflows/codeql.yml`: CodeQL security scanning

**Code Review Checklist:**
- [ ] Code follows project style guidelines
- [ ] Tests added/updated for new features
- [ ] No sensitive data in logs/errors
- [ ] Error handling implemented
- [ ] Security implications reviewed
- [ ] CI must pass before merge

## Important Architecture Decisions

1. **Model Server as Gateway**: The model_server is NOT a local vLLM deployment by default. It's a gateway to external AI providers (OpenAI, Anthropic, Google, ZAI). Local vLLM is optional.

2. **Service Discovery**: All services use Docker's internal DNS via `aigarage-network` bridge network. Service names are: `aigarage-backend`, `aigarage-model-server`, `aigarage-frontend`, `aigarage-nginx`.

3. **Health Checks**: All services have health checks using wget or curl. Nginx waits for backend, model-server, and frontend to be healthy before starting.

4. **Frontend Hot Reload**: Development mode uses volume mounts to enable hot reload. Changes in `web/` are immediately reflected without rebuilding containers.

5. **Logging**:
   - Backend: Structured logs to `backend/app.log` with custom Gin logger
   - Model server: JSON structured logging (use structlog or standard logging)
   - All services: Log to stdout/stderr for Docker container logs

6. **Environment Management**: Use environment-specific files:
   - Local: `.env` (copy from `.env.example`)
   - Docker dev: `docker/.env.development`
   - Docker prod: `docker/.env.production`
   - Base Docker: `docker/.env`

## Documentation Requirements

**MUST:**
- Document all public APIs
- Include README in each major directory
- Document environment variables in `.env.example`
- Update CLAUDE.md for architectural changes

**SHOULD:**
- Include code examples in documentation
- Use diagrams for complex flows
- Document architectural decisions (ADRs)
- Keep documentation synchronized with code
