DOCKER_USERNAME = pyso
APP_NAME = nasa
VERSION = 0.0.0dev1

.PHONY: help build push deploy version clean test

help:
	@echo "Available commands:"
	@echo "  make build      - Build Docker image"
	@echo "  make push       - Push image to Docker Hub"
	@echo "  make deploy     - Build and push"
	@echo "  make version    - Show current version"
	@echo "  make clean      - Remove local images"
	@echo "  make test       - Test the image"

build:
	docker build --build-arg APP_VERSION=$(VERSION) -t $(DOCKER_USERNAME)/$(APP_NAME):$(VERSION) .
	docker tag $(DOCKER_USERNAME)/$(APP_NAME):$(VERSION) $(DOCKER_USERNAME)/$(APP_NAME):latest

push:
	docker push $(DOCKER_USERNAME)/$(APP_NAME):$(VERSION)
	docker push $(DOCKER_USERNAME)/$(APP_NAME):latest

deploy: build push
	@echo "Deployed version $(VERSION)"

version:
	@echo "Current version: $(VERSION)"

clean:
	docker rmi $(DOCKER_USERNAME)/$(APP_NAME):$(VERSION) || true
	docker rmi $(DOCKER_USERNAME)/$(APP_NAME):latest || true

test:
	docker run --rm $(DOCKER_USERNAME)/$(APP_NAME):$(VERSION) --help
