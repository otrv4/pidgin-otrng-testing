DOCKER_IMAGE="otr4/pidgin-plugin-testing"

default:
	pytest

deps:
	pip install --user -r requirements.txt

clean:
	rm -rf base_purple/prefs.xml

test:
	sudo docker run -t \
		-v $(shell pwd):/src:Z \
		-v $(shell pwd)/dogtail-root:/tmp/dogtail-root:Z \
		$(DOCKER_IMAGE) pytest

docker-debug:
	sudo docker run -t --net=host \
		-e "ENABLE_DEBUG=true" --rm \
		-v $(shell pwd):/src:Z \
		-v $(shell pwd)/dogtail-root:/tmp/dogtail-root:Z \
		-p 5222:5222 -p 5900:5900 \
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

docker-kill: clean
	sudo docker kill `(sudo docker ps -q --filter ancestor=$(DOCKER_IMAGE))`

