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

2. **Model Server** (`model_server/`): Python FastAPI + vLLM service
   - Entry point: `server.py` (run as module: `python -m model_server.server`)
   - Uses FastAPI with uvicorn for OpenAI-compatible API
   - Provides `/v1/chat/completions` endpoint
   - Requires `MODEL_PATH` environment variable
   - Default port: 8000 (configurable via `PORT` env var)
   - Python tooling configured in `pyproject.toml` (black, isort, mypy)

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

**Testing and Linting:**
```bash
cd backend
# Run tests (if tests exist)
go test -v -race ./...

# Run go vet
go vet ./...

# Run golangci-lint (uses backend/.golangci.yml config)
golangci-lint run --config=.golangci.yml

# Format code
go fmt ./...
```

### Model Server (Python)
```bash
cd model_server
export MODEL_PATH=/path/to/model
export PORT=8000  # optional, defaults to 8000
python -m model_server.server
```

**Code Quality and Testing:**
```bash
cd model_server
# Format code with black
black .

# Sort imports with isort
isort .

# Type check with mypy (configured in pyproject.toml)
mypy .

# Lint with flake8
flake8 . --max-line-length=88

# Run tests (if tests exist)
pytest
```

### Frontend (Vue)
```bash
cd web
npm install
npm run dev      # Development server on :7016
npm run build    # Production build (includes type checking via vue-tsc)
npm run preview  # Preview production build
```

**Linting and Type Checking:**
```bash
cd web
# Type check (strict mode enabled)
npx vue-tsc --noEmit

# ESLint (if configured)
npx eslint . --ext .vue,.js,.ts
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
- `BACKEND_PATH`: Path to backend directory (used by start.sh, default: `backend`)

**Note:** The `.env.example` file is currently minimal. You may need to add variables directly to `.env` based on your setup.

## Key Dependencies

- **Backend**: Gin web framework (Go 1.23.4)
- **Model Server**: vllm==0.8.1, uvicorn, fastapi
- **Frontend**: Vue 3, Element Plus, Vue Router, Vite

## Project Structure Notes

- `lib/`: Shared Go library (linked via go.mod replace directive) - currently empty, reserved for future shared code
- `nginx/`: Reverse proxy configuration for production
- `log/`: Application logs (backend.log, build.log, start.log)
- The `start.sh` script manages the backend process lifecycle with PID tracking

**Service Communication:**
- Frontend (port 7016) → Backend (port 8080) → Model Server (port 8000)
- The Go backend acts as a gateway, handling business logic and forwarding requests to the Python model server
- Model server provides OpenAI-compatible `/v1/chat/completions` endpoint for LLM inference

---

## Development Standards and Guidelines

### 1. Frontend Development Rules (Vue 3 + TypeScript)

#### A. Type Definition Standards

**MUST:**
- Use explicit type annotations for all component props, emits, and refs
- Define interfaces for all API response types
- Enable strict mode in TypeScript (already configured in `tsconfig.app.json`)
- Use `unknown` instead of `any` for types that are truly unknown at compile time
- Type all function parameters and return values

**TypeScript Configuration:**
- Strict mode is enabled with additional checks: `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`, `noUncheckedSideEffectImports`
- Type checking is performed during `npm run build` via vue-tsc
- For standalone type checks without building: `npx vue-tsc --noEmit`

**MUST NOT:**
- Use `any` type except in migration code with TODO comments
- Use implicit `any` by omitting type annotations
- Use `as` assertions without proper type guards

**SHOULD:**
- Use discriminated unions for complex state types
- Leverage TypeScript's type inference for obvious cases (e.g., `const count = ref(0)`)
- Create shared types in `web/src/types/` directory
- Use utility types (`Partial<T>`, `Pick<T>`, `Omit<T>`) to derive types

**EXAMPLE:**
```typescript
// GOOD - Explicit types with interfaces
interface User {
  id: string
  name: string
  email: string
}

interface ApiResponse<T> {
  data: T
  status: number
  message: string
}

// Function with explicit return type
async function fetchUser(id: string): Promise<ApiResponse<User>> {
  const response = await fetch(`/api/users/${id}`)
  return response.json()
}

// BAD - Using any
function processData(data: any) { } // Avoid
```

#### B. Component Design Principles

**MUST:**
- Use Composition API with `<script setup>` syntax (already established in codebase)
- Define component props using `defineProps<T>()` with TypeScript generics
- Define emits using `defineEmits<T>()` with type signatures
- Use `scoped` CSS for component-specific styles (current pattern in codebase)
- Keep components under 300 lines; split if larger

**MUST NOT:**
- Use Options API for new components
- Mix global and scoped CSS without clear separation
- Create deeply nested component hierarchies (>5 levels)

**SHOULD:**
- Name components using PascalCase (current pattern: `NavBar.vue`, `Home.vue`)
- Organize components by feature:
  - `web/src/components/` - Reusable components
  - `web/src/view/` - Page-level components
  - `web/src/composables/` - Reusable composition functions
- Use `<script setup lang="ts">` consistently
- Extract reusable logic into composables

**EXAMPLE:**
```typescript
// GOOD - Component with explicit types
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
</script>

// BAD - Options API or missing types
<script lang="ts">
export default {
  props: {
    title: String // Avoid - loses type safety
  }
}
</script>
```

#### C. State Management Patterns

**MUST:**
- Use `ref<T>()` for primitive values and reactive objects
- Use `reactive<T>()` for complex nested objects
- Use `computed<T>()` for derived state
- Maintain immutable update patterns for complex state

**MUST NOT:**
- Mutate props directly
- Share state between unrelated components without proper state management
- Use `watch` when `computed` is more appropriate

**SHOULD:**
- Use Pinia for global state when adding it (currently not in dependencies)
- Keep local state in components for simple cases
- Use composables for shared reactive logic
- Follow Vue 3 reactivity best practices

**STATE HIERARCHY:**
1. **Local State**: Component-scoped (`ref`, `reactive`)
2. **Composables**: Shared logic across components
3. **Global State**: App-wide state (use Pinia when needed)

**EXAMPLE:**
```typescript
// GOOD - Immutable updates
const state = ref<User[]>([])

function addUser(user: User) {
  state.value = [...state.value, user] // Immutable
}

// GOOD - Using computed for derived state
const totalCount = computed(() => state.value.length)

// BAD - Direct mutation
state.value.push(user) // Avoid in some contexts
```

---

### 2. Backend API Development Rules (Go + Gin)

#### A. API Design Standards

**MUST:**
- Follow RESTful principles for resource naming
- Use appropriate HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Return consistent JSON response structure
- Include HTTP status codes according to RFC 9110
- Support pagination for list endpoints with `page` and `page_size` query parameters

**MUST NOT:**
- Return nested resources beyond 3 levels
- Use verbs in endpoint paths (e.g., `/getUsers`)
- Mix data formats (always return JSON)

**SHOULD:**
- Use plural nouns for resource collections (`/api/users`, not `/api/user`)
- Version APIs via URL path (`/api/v1/...`)
- Include pagination metadata in list responses
- Use kebab-case for query parameters

**STANDARD RESPONSE FORMAT:**
```go
// Success Response
type ApiResponse struct {
    Data    interface{} `json:"data"`
    Status  int         `json:"status"`
    Message string      `json:"message,omitempty"`
}

// Paginated Response
type PaginatedResponse struct {
    Data       interface{} `json:"data"`
    Pagination Pagination  `json:"pagination"`
    Status     int         `json:"status"`
}

type Pagination struct {
    Page       int `json:"page"`
    PageSize   int `json:"page_size"`
    TotalCount int `json:"total_count"`
    TotalPages int `json:"total_pages"`
}
```

**ENDPOINT EXAMPLES:**
```
GET    /api/v1/users              - List users (paginated)
GET    /api/v1/users/:id          - Get user by ID
POST   /api/v1/users              - Create user
PUT    /api/v1/users/:id          - Update user
DELETE /api/v1/users/:id          - Delete user
GET    /api/v1/users/:id/posts    - Get user's posts (nested resource)
```

#### B. Error Handling Guidelines

**MUST:**
- Return consistent error response format
- Include user-friendly error messages (no stack traces in API responses)
- Log detailed errors server-side (current pattern: `app.log`)
- Use appropriate HTTP status codes for errors
- Never expose sensitive information in error messages

**ERROR RESPONSE FORMAT:**
```go
type ErrorResponse struct {
    Error   ErrorDetail `json:"error"`
    Status  int         `json:"status"`
    Path    string      `json:"path,omitempty"`
}

type ErrorDetail struct {
    Code    string `json:"code"`      // e.g., "VALIDATION_ERROR"
    Message string `json:"message"`   // User-friendly message
    Details string `json:"details,omitempty"` // Additional context
}
```

**HTTP STATUS CODE USAGE:**
```go
200 OK              - Successful GET, PUT, PATCH
201 Created         - Successful POST
204 No Content      - Successful DELETE
400 Bad Request     - Validation errors
401 Unauthorized    - Missing or invalid authentication
403 Forbidden       - Valid auth but insufficient permissions
404 Not Found       - Resource doesn't exist
409 Conflict        - Resource already exists
422 Unprocessable   - Semantic errors
500 Internal Error  - Unexpected server errors
```

**EXAMPLE:**
```go
// GOOD - Proper error handling
func GetUser(c *gin.Context) {
    id := c.Param("id")

    user, err := userService.FindByID(id)
    if err != nil {
        logger.Printf("Error finding user %s: %v", id, err)

        if errors.Is(err, ErrNotFound) {
            c.JSON(404, gin.H{
                "error": gin.H{
                    "code": "NOT_FOUND",
                    "message": "User not found",
                },
                "status": 404,
            })
            return
        }

        c.JSON(500, gin.H{
            "error": gin.H{
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            },
            "status": 500,
        })
        return
    }

    c.JSON(200, gin.H{
        "data": user,
        "status": 200,
    })
}
```

#### C. Security Requirements

**MUST:**
- Implement authentication for all non-public endpoints
- Validate and sanitize all input data
- Use parameterized queries to prevent SQL injection
- Set appropriate CORS headers
- Implement rate limiting for API endpoints
- Never log sensitive data (passwords, tokens, API keys)

**SHOULD:**
- Use HTTPS in production
- Implement request signing for sensitive operations
- Add request ID tracking for audit logs
- Validate Content-Type headers
- Use security headers (helmet middleware equivalent)

**EXAMPLE:**
```go
// Input validation middleware
func validateJSON() gin.HandlerFunc {
    return func(c *gin.Context) {
        if c.Request.Header.Get("Content-Type") != "application/json" {
            c.JSON(415, gin.H{
                "error": gin.H{
                    "code": "UNSUPPORTED_MEDIA_TYPE",
                    "message": "Content-Type must be application/json",
                },
                "status": 415,
            })
            c.Abort()
            return
        }
        c.Next()
    }
}

// Rate limiting middleware
func rateLimit() gin.HandlerFunc {
    // Implement rate limiting logic
}
```

#### D. Code Quality Standards

**MUST:**
- Follow standard Go project layout
- Use `gofmt` for code formatting
- Handle all errors explicitly
- Write godoc comments for exported functions
- Use meaningful variable names

**SHOULD:**
- Use `golangci-lint` for static analysis
- Follow Effective Go guidelines
- Write unit tests for business logic
- Keep functions under 50 lines
- Use interfaces for dependency injection

---

### 3. Python Development Rules (FastAPI + vLLM)

#### A. Type Hints and Annotations

**MUST:**
- Use type hints for all function parameters and return values
- Define Pydantic models for all request/response bodies
- Use `typing` module for complex types (List, Dict, Optional, etc.)
- Type all class attributes

**MUST NOT:**
- Use bare `except:` clauses
- Mix `None` returns with typed returns without `Optional`

**SHOULD:**
- Use modern type hints (Python 3.9+ style: `list[str]` instead of `List[str]`)
- Create strict Pydantic models with validation
- Use `TypeAlias` for complex repeated types
- Enable `mypy` strict mode if possible

**EXAMPLE:**
```python
# GOOD - Full type hints with Pydantic
from pydantic import BaseModel, Field
from typing import Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., min_length=1, max_length=4096)

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: str
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=2048, gt=0)

class ChatResponse(BaseModel):
    content: str
    finish_reason: str
    usage: dict[str, int]

async def generate_completion(request: ChatRequest) -> ChatResponse:
    """Generate chat completion using vLLM."""
    # Implementation
    pass

# BAD - Missing type hints
def generate_completion(request):
    # Avoid
    pass
```

#### B. API Development Standards

**MUST:**
- Use async/await for I/O operations
- Define OpenAPI documentation for all endpoints
- Return Pydantic models for responses
- Validate all request data with Pydantic
- Use appropriate HTTP status codes

**SHOULD:**
- Organize routes using FastAPI Router
- Use dependency injection for shared logic
- Implement request validation
- Add comprehensive error handlers
- Use API versioning in path (`/v1/...`)

**EXAMPLE:**
```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AiGarage Model Server",
    description="vLLM-based inference server",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:7016"],  # Frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    "/v1/chat/completions",
    response_model=ChatResponse,
    summary="Generate chat completion",
    description="Generates a chat completion using the configured LLM model"
)
async def create_chat_completion(
    request: ChatRequest,
    api_key: str = Depends(validate_api_key)
) -> ChatResponse:
    try:
        # Implementation using vLLM
        result = await vllm_generate(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

#### C. Code Style and Formatting

**MUST:**
- Follow PEP 8 style guide
- Use `black` for code formatting
- Use `isort` for import sorting
- Set line length to 88 characters (black default)

**SHOULD:**
- Use `flake8` for linting
- Enable `pylint` for additional checks
- Use `ruff` as a faster alternative to flake8 + isort
- Configure pre-commit hooks

**`.pre-commit-config.yaml` for Python:**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
```

#### D. vLLM Integration Patterns

**MUST:**
- Maintain backward compatibility with OpenAI API format
- Handle model loading errors gracefully
- Validate model path before starting server
- Log generation metrics

**SHOULD:**
- Implement request batching optimization
- Add health check endpoint
- Monitor GPU memory usage
- Cache frequently used prompts

**EXAMPLE:**
```python
# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if the model server is healthy."""
    try:
        if MODEL_PATH and os.path.exists(MODEL_PATH):
            return {"status": "healthy", "model_loaded": True}
        return {"status": "healthy", "model_loaded": False}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service unavailable")

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Return server metrics."""
    return {
        "requests_processed": stats.total_requests,
        "avg_generation_time": stats.avg_time,
        "gpu_memory_usage": get_gpu_memory()
    }
```

---

### 4. Automation and Quality Assurance Rules

#### A. Pre-commit Hooks

**MUST:**
- Run type checkers before commit
- Run code formatters
- Run basic linters
- Validate configuration files

**RECOMMENDED `.pre-commit-config.yaml`:**
```yaml
repos:
  # Frontend hooks
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        files: ^(web/.*\.(ts|tsx|vue))$
        args: [--fix]

  # Python hooks
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        files: ^(model_server/.*\.py)$

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort
        files: ^(model_server/.*\.py)$

  # Go hooks
  - repo: https://github.com/golangci/golangci-lint
    rev: v1.55.2
    hooks:
      - id: golangci-lint
        files: ^(backend/.*\.go)$

  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-json
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-added-large-files
```

#### B. CI/CD Pipeline Standards

**EXISTING WORKFLOWS:**
- `.github/workflows/ci.yml` - Full CI pipeline for all three services
- `.github/workflows/codeql.yml` - CodeQL security scanning

The CI workflow already includes:
- Automated testing on push/PR to main, develop, and feature/* branches
- Type checking for TypeScript (vue-tsc via build)
- Go tests, vet, and build
- Python black, isort, flake8, mypy checks
- Security scanning with Trivy
- Dependency review for PRs

#### C. Code Review Guidelines

**MUST:**
- All code requires at least one approval before merging
- CI must pass before merge
- PR descriptions must explain "why" not just "what"
- No merge conflicts allowed

**SHOULD:**
- Keep PRs focused and under 500 lines
- Request review from team members familiar with the area
- Respond to all review comments
- Update PR description based on review feedback

**REVIEW CHECKLIST:**
- [ ] Code follows project style guidelines
- [ ] Tests added/updated for new features
- [ ] Documentation updated
- [ ] No sensitive data in logs/errors
- [ ] Error handling implemented
- [ ] Performance implications considered
- [ ] Security implications reviewed

---

### 5. Additional Project-Specific Standards

#### A. Go Code Conventions

**FILE STRUCTURE:**
```
backend/
├── main.go              # Entry point
├── go.mod
├── go.sum
├── handlers/            # HTTP handlers
│   └── user.go
├── services/            # Business logic
│   └── user.go
├── models/              # Data models
│   └── user.go
├── middleware/          # Gin middleware
│   └── auth.go
└── config/              # Configuration
    └── config.go
```

**NAMING CONVENTIONS:**
- Filenames: `snake_case.go`
- Package names: lowercase, single word
- Exported functions/variables: `PascalCase`
- Private functions/variables: `camelCase`
- Constants: `PascalCase` or `UPPER_SNAKE_CASE`
- Interfaces: `PascalCase` ending with `-er` suffix

**EXAMPLE:**
```go
// package: handlers
// file: user_handler.go

package handlers

import (
    "github.com/gin-gonic/gin"
)

type UserHandler struct {
    userService *services.UserService
}

func NewUserHandler(userService *services.UserService) *UserHandler {
    return &UserHandler{userService: userService}
}

func (h *UserHandler) GetByID(c *gin.Context) {
    // Handler logic
}
```

#### B. Docker and Container Standards

**MUST:**
- Use multi-stage builds for production images
- Tag images with semantic version
- Run containers as non-root user
- Use specific version tags (not `latest`)
- Include health check in Docker images

**SHOULD:**
- Optimize layer caching (order commands by change frequency)
- Use `.dockerignore` files
- Scan images for vulnerabilities
- Document container requirements

**EXAMPLE `Dockerfile` pattern:**
```dockerfile
# Multi-stage build for Go backend
FROM golang:1.23.4-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o server main.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/server .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ping || exit 1
CMD ["./server"]
```

#### C. Logging and Monitoring

**MUST:**
- Use structured logging (JSON format)
- Include correlation IDs for request tracking
- Log at appropriate levels (ERROR, WARN, INFO, DEBUG)
- Never log sensitive data

**SHOULD:**
- Include context in log messages
- Use consistent log format across services
- Implement log rotation
- Monitor log aggregation

**EXAMPLE (Go):**
```go
import "log/slog"

logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

logger.Info("User created",
    "user_id", user.ID,
    "email", user.Email,
    "request_id", requestID,
)
```

**EXAMPLE (Python):**
```python
import structlog

logger = structlog.get_logger()
logger.info("user_created", user_id=user.id, email=user.email)
```

#### D. Documentation Requirements

**MUST:**
- Document all public APIs
- Include README in each major directory
- Document environment variables
- Update CLAUDE.md for architectural changes

**SHOULD:**
- Include code examples
- Use diagrams for complex flows
- Keep documentation up-to-date with code
- Document architectural decisions (ADRs)
