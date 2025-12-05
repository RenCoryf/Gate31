#!/bin/bash
curl -X POST "http://127.0.0.1:8000/match" \
  -F "file=@$(pwd)/matcher/tests/3.jpg"

