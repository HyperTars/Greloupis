LINTER = flake8
BACKEND_DIR = backend
FRONTEND_DIR = frontend
REQ_DIR = requirements
TAG = latest
DOCKER_REPO = hypertars/greloupis

FORCE:

prod:	dev_env tests github

dev_env:	dev_env_backend dev_env_frontend

github:	FORCE
	- git commit -a
	- git push origin

tests:
	cd $(BACKEND_DIR); make tests
	cd $(FRONTEND_DIR); make tests

docs:	#FORCE
	cd $(BACKEND_DIR); make docs

report:
	cd $(BACKEND_DIR); make report
	cd $(FRONTEND_DIR); make report

coverage:
	cd $(BACKEND_DIR); make coverage

# For both frontend and backend
docker_build:
	docker-compose build

docker_run:
	docker-compose up

docker_status:
	docker-compose ps

docker_push:
	- docker login --username $(DOCKER_USER) --password $(DOCKER_PASS)
	- docker-compose build --pull
	- docker-compose push

docker_clean:
	- docker stop $(docker ps -aq)
	- docker system prune -a

docker_build_backend:
	cd $(BACKEND_DIR); make docker_build

docker_build_frontend:
	cd $(FRONTEND_DIR); make docker_build

docker_push_backend:
	cd $(BACKEND_DIR); make docker_push

docker_push_frontend:
	cd $(FRONTEND_DIR); make docker_push

# Build and Run from local Docker build (for development tests)
docker_run_backend_build: docker_build_backend
	cd $(BACKEND_DIR); docker_run

docker_run_frontend_build: docker_build_frontend
	cd $(FRONT_DIR); docker_run

# Run from Docker Hub (for fast use)
docker_run_backend_hub:
	cd $(BACKEND_DIR); make docker_hub

docker_run_frontend_hub:
	cd $(FRONTEND_DIR); make docker_hub

# Run from native python or npm (for Dockerfile use)
run_backend:
	cd $(BACKEND_DIR); make run_backend

run_frontend:
	cd $(FRONTEND_DIR); make run_frontend

# build dev env (for Dockerfile use)
dev_env_backend:
	cd $(BACKEND_DIR); make dev_env_backend

dev_env_frontend:
	cd $(FRONTEND_DIR); make dev_env_frontend

# Heroku
heroku:
	cd $(FRONTEND_DIR); make heroku
	cd $(BACKEND_DIR); make heroku