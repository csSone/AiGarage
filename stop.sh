#!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Configuration
DOCKER_DIR="${SCRIPT_DIR}/docker"
LOG_DIR="${SCRIPT_DIR}/log"

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

# Logging function
log_message() {
    echo "$(date): $1" >> "${LOG_DIR}/stop.log"
}

# Check if Docker is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_message "Warning: Docker is not available, skipping Docker services"
        return 1
    fi

    if ! docker info &> /dev/null; then
        log_message "Warning: Docker daemon is not running, skipping Docker services"
        return 1
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_message "Warning: docker-compose is not available, skipping Docker services"
        return 1
    fi

    return 0
}

# Stop Docker services
stop_docker_services() {
    if [ ! -d "${DOCKER_DIR}" ]; then
        log_message "Docker directory not found: ${DOCKER_DIR}"
        return 1
    fi

    log_message "Stopping Docker services..."

    cd "${DOCKER_DIR}"

    # Check if docker-compose.yml exists
    if [ ! -f "docker-compose.yml" ]; then
        log_message "docker-compose.yml not found in ${DOCKER_DIR}"
        cd "${SCRIPT_DIR}"
        return 1
    fi

    # Stop and remove containers
    if docker-compose ps -q &> /dev/null; then
        log_message "Stopping Docker containers..."
        docker-compose down >> "${LOG_DIR}/stop.log" 2>&1
        if [ $? -eq 0 ]; then
            log_message "Docker services stopped successfully"
        else
            log_message "Failed to stop Docker services, check ${LOG_DIR}/stop.log for details"
        fi
    else
        log_message "No Docker services are currently running"
    fi

    cd "${SCRIPT_DIR}"
}

# Stop model server (if running separately)
stop_model_server() {
    local model_server_pid_file="${SCRIPT_DIR}/model_server.pid"

    if [ -f "${model_server_pid_file}" ]; then
        local model_server_pid=$(cat "${model_server_pid_file}")

        if ps -p $model_server_pid > /dev/null 2>&1; then
            log_message "Stopping model server (PID: ${model_server_pid})..."
            kill $model_server_pid

            # Wait a moment for graceful shutdown
            sleep 3

            # Force kill if still running
            if ps -p $model_server_pid > /dev/null 2>&1; then
                log_message "Force killing model server (PID: ${model_server_pid})..."
                kill -9 $model_server_pid
            fi

            log_message "Model server stopped"
        else
            log_message "Model server PID file exists but process not running"
        fi

        rm -f "${model_server_pid_file}"
    else
        log_message "Model server PID file not found"
    fi
}

# Stop legacy backend service (for compatibility)
stop_legacy_backend() {
    local backend_pid_file="${SCRIPT_DIR}/backend/backend.pid"

    if [ -f "${backend_pid_file}" ]; then
        local backend_pid=$(cat "${backend_pid_file}")

        if ps -p $backend_pid > /dev/null 2>&1; then
            log_message "Stopping legacy backend service (PID: ${backend_pid})..."
            kill $backend_pid

            # Wait a moment for graceful shutdown
            sleep 2

            # Force kill if still running
            if ps -p $backend_pid > /dev/null 2>&1; then
                log_message "Force killing legacy backend service (PID: ${backend_pid})..."
                kill -9 $backend_pid
            fi

            log_message "Legacy backend service stopped"
        else
            log_message "Legacy backend PID file exists but process not running"
        fi

        rm -f "${backend_pid_file}"
    else
        log_message "Legacy backend PID file not found"
    fi
}

# Clean up resources
cleanup_resources() {
    log_message "Cleaning up resources..."

    # Remove temporary files
    find "${SCRIPT_DIR}" -name "*.pid" -type f -exec rm -f {} \; 2>/dev/null

    # Clean up old logs (keep last 7 days)
    find "${LOG_DIR}" -name "*.log" -type f -mtime +7 -exec rm -f {} \; 2>/dev/null

    log_message "Resource cleanup completed"
}

# Show status after stopping
show_status() {
    log_message "Final status check..."

    # Check for any remaining processes
    local remaining_processes=0

    # Check model server
    local model_server_pid_file="${SCRIPT_DIR}/model_server.pid"
    if [ -f "${model_server_pid_file}" ]; then
        local model_server_pid=$(cat "${model_server_pid_file}")
        if ps -p $model_server_pid > /dev/null 2>&1; then
            log_message "Warning: Model server still running (PID: ${model_server_pid})"
            remaining_processes=$((remaining_processes + 1))
        fi
    fi

    # Check legacy backend
    local backend_pid_file="${SCRIPT_DIR}/backend/backend.pid"
    if [ -f "${backend_pid_file}" ]; then
        local backend_pid=$(cat "${backend_pid_file}")
        if ps -p $backend_pid > /dev/null 2>&1; then
            log_message "Warning: Legacy backend still running (PID: ${backend_pid})"
            remaining_processes=$((remaining_processes + 1))
        fi
    fi

    # Check Docker containers
    if check_docker; then
        cd "${DOCKER_DIR}"
        local running_containers=$(docker-compose ps -q 2>/dev/null | wc -l)
        if [ "$running_containers" -gt 0 ]; then
            log_message "Warning: ${running_containers} Docker containers still running"
            remaining_processes=$((remaining_processes + running_containers))
        fi
        cd "${SCRIPT_DIR}"
    fi

    if [ $remaining_processes -eq 0 ]; then
        log_message "All services stopped successfully"
        echo " All AiGarage services have been stopped"
    else
        log_message "Warning: ${remaining_processes} services/processes may still be running"
        echo "  Some services may still be running. Check logs for details."
    fi
}

# Main execution
main() {
    echo "Stopping AiGarage services..."
    log_message "Starting shutdown process..."

    # Stop services in order
    stop_model_server
    stop_docker_services
    stop_legacy_backend

    # Clean up
    cleanup_resources

    # Show final status
    show_status
}

# Handle script interruption
cleanup_on_interrupt() {
    echo ""
    log_message "Shutdown interrupted by user"
    exit 130
}

# Set up signal handlers
trap cleanup_on_interrupt INT TERM

# Execute main function
main "$@"