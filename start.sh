#!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source environment files
source ~/.bashrc
if [ -f "${SCRIPT_DIR}/.env" ]; then
    source "${SCRIPT_DIR}/.env"
fi

# Docker and logging configuration
DOCKER_DIR="${SCRIPT_DIR}/docker"
LOG_DIR="${SCRIPT_DIR}/log"
COMPOSE_FILE="${DOCKER_DIR}/docker-compose.yml"

# Ensure log directory exists and clean start log
mkdir -p "${LOG_DIR}"
> "${LOG_DIR}/start.log"

# Logging function
log_message() {
    echo "$(date): $1" >> "${LOG_DIR}/start.log"
}

# Check if Docker is installed and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_message "Error: Docker is not installed or not in PATH"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        log_message "Error: Docker daemon is not running"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_message "Error: docker-compose or docker compose is not installed"
        exit 1
    fi

    log_message "Docker environment check passed"
}

# Check environment variables
check_environment() {
    local required_vars=()
    local optional_vars=()

    # Check for model server environment if running separately
    if [ "${SKIP_MODEL_SERVER}" != "true" ]; then
        required_vars+=("MODEL_PATH")
    fi

    # Optional variables with defaults
    optional_vars+=("PORT:8000")
    optional_vars+=("BACKEND_PATH:backend")

    # Check required variables
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            log_message "Error: Required environment variable $var is not set"
            exit 1
        fi
    done

    # Set optional variables with defaults
    for var_def in "${optional_vars[@]}"; do
        IFS=':' read -r var_name default_value <<< "$var_def"
        if [ -z "${!var_name}" ]; then
            export "$var_name"="$default_value"
            log_message "Setting $var_name to default value: $default_value"
        fi
    done

    log_message "Environment variables check completed"
}

# Start Docker services
start_docker_services() {
    log_message "Starting Docker services..."

    cd "${DOCKER_DIR}"

    # Stop any existing services
    if docker-compose ps -q &> /dev/null; then
        log_message "Stopping existing Docker services..."
        docker-compose down >> "${LOG_DIR}/start.log" 2>&1
    fi

    # Build and start services
    log_message "Building and starting Docker services..."
    if ! docker-compose up -d --build >> "${LOG_DIR}/start.log" 2>&1; then
        log_message "Failed to start Docker services, check ${LOG_DIR}/start.log for details"
        cd "${SCRIPT_DIR}"
        exit 1
    fi

    # Wait for services to be ready
    log_message "Waiting for services to be ready..."
    sleep 10

    # Check service status
    if ! docker-compose ps >> "${LOG_DIR}/start.log" 2>&1; then
        log_message "Failed to get service status"
        cd "${SCRIPT_DIR}"
        exit 1
    fi

    log_message "Docker services started successfully"
    cd "${SCRIPT_DIR}"
}

# Start model server separately (if needed)
start_model_server() {
    if [ "${SKIP_MODEL_SERVER}" == "true" ]; then
        log_message "Skipping model server startup (SKIP_MODEL_SERVER=true)"
        return 0
    fi

    if [ -z "${MODEL_PATH}" ]; then
        log_message "Warning: MODEL_PATH not set, skipping model server startup"
        return 0
    fi

    log_message "Starting model server..."

    local model_server_dir="${SCRIPT_DIR}/model_server"
    local model_server_pid_file="${SCRIPT_DIR}/model_server.pid"

    if [ -f "${model_server_pid_file}" ]; then
        local existing_pid=$(cat "${model_server_pid_file}")
        if ps -p $existing_pid > /dev/null 2>&1; then
            log_message "Model server already running with PID ${existing_pid}"
            return 0
        else
            rm -f "${model_server_pid_file}"
        fi
    fi

    cd "${model_server_dir}"

    # Start model server in background
    nohup python server.py > "${LOG_DIR}/model_server.log" 2>&1 &
    local model_server_pid=$!
    echo $model_server_pid > "${model_server_pid_file}"

    log_message "Model server started with PID ${model_server_pid}"
    cd "${SCRIPT_DIR}"
}

# Check services health
check_services() {
    log_message "Checking service health..."

    # Check Docker services
    cd "${DOCKER_DIR}"
    local unhealthy_services=$(docker-compose ps --services --filter "status=running" | wc -l)
    if [ "$unhealthy_services" -eq 0 ]; then
        log_message "Warning: No Docker services are running"
    else
        log_message "Docker services status check passed"
    fi
    cd "${SCRIPT_DIR}"

    # Check model server if running
    local model_server_pid_file="${SCRIPT_DIR}/model_server.pid"
    if [ -f "${model_server_pid_file}" ]; then
        local model_server_pid=$(cat "${model_server_pid_file}")
        if ! ps -p $model_server_pid > /dev/null 2>&1; then
            log_message "Warning: Model server process is not running"
        else
            log_message "Model server is running"
        fi
    fi
}

# Stop services function
stop_services() {
    log_message "Stopping all services..."

    # Stop Docker services
    cd "${DOCKER_DIR}"
    docker-compose down >> "${LOG_DIR}/start.log" 2>&1
    cd "${SCRIPT_DIR}"

    # Stop model server
    local model_server_pid_file="${SCRIPT_DIR}/model_server.pid"
    if [ -f "${model_server_pid_file}" ]; then
        local model_server_pid=$(cat "${model_server_pid_file}")
        if ps -p $model_server_pid > /dev/null 2>&1; then
            kill $model_server_pid
            log_message "Stopped model server (PID: ${model_server_pid})"
        fi
        rm -f "${model_server_pid_file}"
    fi

    log_message "All services stopped"
}

# Cleanup function
cleanup() {
    if [ -z "${CLEANUP_DONE}" ]; then
        CLEANUP_DONE=1
        EXIT_CODE=$?
        log_message "Gracefully exiting..."
        stop_services
        exit $EXIT_CODE
    fi
}

# Main execution
main() {
    log_message "Starting AiGarage services..."

    # Run checks
    check_docker
    check_environment

    # Start services
    start_docker_services
    start_model_server

    log_message "All services started successfully"
    log_message "Frontend accessible at: http://localhost"
    log_message "Nginx reverse proxy configured for port 80/443"

    # Initial health check
    check_services
}

# Register signal handlers
trap cleanup TERM INT EXIT

# Start services
main

# Monitoring loop
while true; do
    check_services
    sleep 30
done