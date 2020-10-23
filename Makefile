.PHONY: build clean clean-test clean-pyc clean-build
NAME	:= ghcr.io/clayman-micro/shortner
VERSION ?= latest

CWD := ${PWD}


clean: clean-build clean-image clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-image:
	docker images -qf dangling=true | xargs docker rmi

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr tests/coverage
	rm -f tests/coverage.xml

install: clean
	poetry install

run:
	poetry run python3 -m shortner --debug server run --host=0.0.0.0 \
		--tags='develop' \
		--tags='v0.2.4' \
		--tags='traefik.enable=true' \
		--tags='traefik.http.routers.shortner.rule=Host(`shortner.dev.clayman.pro`)' \
		--tags='traefik.http.routers.shortner.entrypoints=web' \
		--tags='traefik.http.routers.shortner.service=shortner' \
		--tags='traefik.http.routers.shortner.middlewares=shortner-redirect@consulcatalog' \
		--tags='traefik.http.routers.shortner-secure.rule=Host(`shortner.dev.clayman.pro`)' \
		--tags='traefik.http.routers.shortner-secure.entrypoints=websecure' \
		--tags='traefik.http.routers.shortner-secure.service=shortner' \
		--tags='traefik.http.routers.shortner-secure.tls=true' \
		--tags='traefik.http.middlewares.shortner-redirect.redirectscheme.scheme=https' \
		--tags='traefik.http.middlewares.shortner-redirect.redirectscheme.permanent=true'

lint:
	poetry run flake8 src/shortner tests
	poetry run mypy src/shortner tests

test:
	py.test

test-all:
	tox

build:
	docker build -t ${NAME} .
	docker tag ${NAME} ${NAME}:$(VERSION)

publish:
	docker login -u $(DOCKER_USER) -p $(DOCKER_PASS)
	docker push ${NAME}:$(VERSION)

deploy:
	docker run --rm -it -v ${PWD}:/github/workspace --workdir /github/workspace -e SHORTNER_VERSION=$(VERSION) -e VAULT_ADDR=$(VAULT_ADDR) -e VAULT_ROLE_ID=$(VAULT_ROLE_ID) -e VAULT_SECRET_ID=$(VAULT_SECRET_ID) ghcr.io/clayman-micro/action-deploy -i ansible/inventory ansible/deploy.yml
