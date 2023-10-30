#!/bin/bash

# build the docker container
docker buildx build --platform=linux/x86_64 -t newschat .

# run the app
docker run -p 5000:5000 newschat