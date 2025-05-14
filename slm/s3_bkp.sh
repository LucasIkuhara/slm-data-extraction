#!/bin/sh
hcp profile init --vault-secrets
hcp vs run -- aws s3 cp results s3://slm-extractor/results --recursive
