#!/bin/bash

python -m grpc_tools.protoc \
  -I ./protos \
  --python_out=./src/sl5api/pb --pyi_out=./src/sl5api/pb \
  --grpc_python_out=./src/sl5api/pb \
  ./protos/*.proto