#!/bin/sh
doppler run -- aws s3 cp ../plain-pages s3://slm-extractor/plain-pages --recursive
doppler run -- aws s3 cp s3://slm-extractor/plain-pages ../plain-pages --recursive
