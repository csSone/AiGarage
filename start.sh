#!/bin/bash

# source env
source ~/.bashrc
source .env


# backend's pid file
BACKEND_PID_FILE="${SCRIPT_DIR}/${BACKEND_PATH}/backend.pid"

# auto add go to path
add_go_to_path() {
    # check go
    if command -v go &> /dev/null; then
        echo "$(date): Go already in PATH: $(which go)" >> ./log/start.log
        return 0
    fi
    
    # download go
    local common_paths=(
        "/usr/local/go/bin"
        "/usr/bin"
        "/bin"
        "$HOME/go/bin"
        "/home/semon/go/bin"
        "/opt/go/bin"
    )
    
    # scan common paths to find go executable
    for path in "${common_paths[@]}"; do
        if [ -x "$path/go" ]; then
            export PATH="$path:$PATH"
            echo "$(date): Found Go in $path, added to PATH" >> ./log/start.log
            return 0
        fi
    done
    
    # if not found, try to find it using find
    echo "$(date): Searching for Go binary..." >> ./log/start.log
    local go_binary
    go_binary=$(find /usr/local /opt /home -name go -type f -executable 2>/dev/null | head -n 1)
    
    if [ -n "$go_binary" ]; then
        local go_dir
        go_dir=$(dirname "$go_binary")
        export PATH="$go_dir:$PATH"
        echo "$(date): Found Go with find command in $go_dir, added to PATH" >> ./log/start.log
        return 0
    fi
    
    # echo "Error: Go binary not found in common locations"
    echo "$(date): Error: Go binary not found in common locations" >> ./log/start.log
    exit 1
}

# check_and_restart_backend() {}
check_backend() {
    if [ -f "${BACKEND_PID_FILE}" ]; then
        BACKEND_PID=$(cat "${BACKEND_PID_FILE}")
        # check if process is running
        if ! ps -p $BACKEND_PID > /dev/null; then
            echo "$(date): Backend service crashed or stopped, exiting..." >> ./log/start.log
            exit 1
        fi
    else
        # if pid file does not exist, start the service
        echo "$(date): Backend service not running, exiting..." >> ./log/start.log
        exit 1
    fi

    return 0
}

# start the backend program
start_backend() {

    echo "$(date): Starting backend service..." > ./log/start.log
    # get into the backend path
    cd "${SCRIPT_DIR}/${BACKEND_PATH}"
    
    if add_go_to_path === 0; then
        # build backend process with full output capture
        if ! go build -o server main.go > "${SCRIPT_DIR}/log/build.log" 2>&1; then
            echo "$(date): Failed to build backend service, check ${SCRIPT_DIR}/log/build.log for details" >> ../log/start.log
            cd "${SCRIPT_DIR}"
            exit 1
        fi
    else
        echo "$(date): Error: Go binary not found in common locations" >> ./log/start.log
        exit 1
    fi

    
    # running bakend process and save the pid
    nohup ${SCRIPT_DIR}/${BACKEND_PATH}/server > "${SCRIPT_DIR}/log/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "${BACKEND_PID_FILE}"
    
    echo "$(date): Backend service started with PID ${BACKEND_PID}" >> ../log/start.log
    # return to working path
    cd "${SCRIPT_DIR}"
}

# stop the backend process
stop_backend() {
    if [ -f "${BACKEND_PID_FILE}" ]; then
        BACKEND_PID=$(cat "${BACKEND_PID_FILE}")
        if ps -p $BACKEND_PID > /dev/null; then
            echo "$(date): Stopping backend service (PID: ${BACKEND_PID})" >> ./log/start.log
            kill $BACKEND_PID
            rm -f "${BACKEND_PID_FILE}"
        else
            echo "$(date): Backend service PID file exists but process not running" >> ./log/start.log
            rm -f "${BACKEND_PID_FILE}"
        fi
    else
        echo "$(date): Backend service PID file not found" >> ./log/start.log
    fi
}


# cleanup backend
cleanup() {
        # check if backend process is running
    if [ -z "${CLEANUP_DONE}" ]; then
        CLEANUP_DONE=1
        EXIT_CODE=$?
        echo "gracefully exiting..." >> ./log/start.log
        stop_backend
        exit $EXIT_CODE
    fi
}

# start backend
start_backend

# register signal handlers
trap cleanup TERM INT EXIT
while true; do 
    check_backend
    sleep 1
done