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

connect:
	- chmod 400 documents/DevOps.pem
	- ssh -i "documents/DevOps.pem" $(EC2_SERVER)

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

# Build and Run from local Docker (for development tests)
docker_build_backend:
	cd $(BACKEND_DIR); make docker_build docker_run

docker_build_frontend:
	cd $(FRONTEND_DIR); make docker_build docker_run

# Run from Docker Hub (for fast use)
docker_run_backend:
	cd $(BACKEND_DIR); make docker_hub

docker_run_frontend:
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
	- docker login --username _ --password=$(HEROKU_API_KEY) registry.heroku.com
	- heroku container:push --recursive --app $(HEROKU_APP_NAME)
	- heroku container:release frontend backend --app $(HEROKU_APP_NAME)