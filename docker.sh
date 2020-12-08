instr() {
    echo "====================================================================="
    echo "* To run both frontend and backend with docker-compose: 'docker.sh --all' or 'docker.sh -a'"
    echo "* To run only backend: 'docker.sh --backend' or 'docker.sh -b'"
    echo "* To run only frontend: 'docker.sh --frontend' or 'docker.sh -f'"
    echo ""
    echo "Frontend URL: http://localhost:3000"
    echo "Backend URL: http://localhost:5000 (Swagger API)"
    echo ""
    echo "Test user: hypertars (both name & password)"
    echo "Test user: milvus (both name & password)"
    echo "Test user: eclipse (both name & password)"
    echo ""
    echo "! It might take up to 3 min to build frontend"
    echo "====================================================================="
}

env() {
    echo "====================================================================="
    echo "Environment Variables Required for Running:"
    echo "ACCESS_KEY_ID1, ACCESS_KEY_ID2, SECRET_KEY1, SECRET_KEY2, AWS_AUTH_KEY"
    echo "See document: documents/EnvironmentSettings.md"
    echo "====================================================================="
}

command -v docker >/dev/null 2>&1 || { echo >&2 "docker is required but it's not installed or running.  Aborting."; exit 1; } 
if [[ -z "${ACCESS_KEY_ID1}" ]] || [[ -z "${ACCESS_KEY_ID2}" ]] || [[ -z "${SECRET_KEY1}" ]] || [[ -z "${SECRET_KEY2}" ]] || [[ -z "${AWS_AUTH_KEY}" ]] || [[ -z "${AWS_CLOUD_FRONT}" ]] || [[ -z "${AWS_THUMBNAIL_FOLDER}" ]] || [[ -z "${MONGO_DEV}" ]] || [[ -z "${MONGO_PROD}" ]] || [[ -z "${MONGO_TEST}" ]] ;
then env exit 0
if [[ $1 = "--help" ]] || [[ $1 = "-h" ]]
then instr exit 0
elif [[ $1 = "--backend" ]] || [[ $1 = "-b" ]]
then make docker_run_backend_build
elif [[ $1 = "--frontend" ]] || [[ $1 = "-f" ]]
then make docker_run_frontend_build
elif [[ $1 = "--all" ]] || [[ $1 = "-a" ]]
then 
    command -v docker-compose >/dev/null 2>&1 || { echo >&2 "docker-compose is required but it's not installed.  Aborting."; exit 1; } 
    make docker_run
else instr exit 0
fi