#!/bin/sh
doppler run -- aws s3 cp results s3://slm-extractor/results --recursive
doppler run -- aws s3 cp s3://slm-extractor/results results --recursive
