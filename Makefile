
build:
	docker build -t audioset_demo .

run:
	docker run -p 10000:8080 --name audioset_demo -itd audioset_demo
