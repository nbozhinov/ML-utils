#!/bin/bash

bazel build --config=opt --config=cuda //tensorflow:libtensorflow.so
bazel build --config=opt --config=cuda //tensorflow:libtensorflow_cc.so
bazel build --config=opt --config=cuda //tensorflow:install_headers
