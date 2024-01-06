#!/bin/sh

docker build --platform linux/amd64 -t scraper .
docker tag scraper eu.gcr.io/valiant-student-408721/scraper
docker push eu.gcr.io/valiant-student-408721/scraper