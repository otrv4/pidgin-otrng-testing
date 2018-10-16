DOCKER_IMAGE="otr4/pidgin-plugin-testing"

default:
	pytest

deps:
	pip install --user -r requirements.txt

test:
	sudo docker run -t \
		-v $(shell pwd):/src:Z \
		-v $(shell pwd)/dogtail-root:/tmp/dogtail-root:Z \
		$(DOCKER_IMAGE) pytest

docker-debug:
	sudo docker run -t \
		-e "ENABLE_DEBUG=true" \
		-v $(shell pwd):/src:Z \
		-v $(shell pwd)/dogtail-root:/tmp/dogtail-root:Z \
		-p 5900:5900 \
		$(DOCKER_IMAGE) pidgin -c /src/base_purple

docker-build:
	sudo docker build -t $(DOCKER_IMAGE) .

docker-term:
	sudo docker run -it -v $(shell pwd):/src:Z $(DOCKER_IMAGE) /bin/bash

docker-run:
	sudo docker run -it \
		-v $(shell pwd):/src:Z \
		-v $(shell pwd)/dogtail-root:/tmp/dogtail-root:Z \
		$(DOCKER_IMAGE) $(RUN)

