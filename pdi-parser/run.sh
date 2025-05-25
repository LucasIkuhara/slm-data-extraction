#!/bin/sh
docker build -t pdi-parser .
docker run -it pdi-parser bash
