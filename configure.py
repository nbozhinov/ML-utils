#!/bin/python

import argparse
from os import path as os_path, chmod
from pathlib import Path
import stat

arch = "x86_64"
# arch = "arm64"
# ubuntu_version_name = "focal"
ubuntu_version_name = "bionic"
# ubuntu_version_numeric = "2004"
ubuntu_version_numeric = "1804"

# 
# https://developer.nvidia.com/tensorrt
# https://developer.nvidia.com/nvidia-tensorrt-7x-download

# Versions taken from https://www.tensorflow.org/install/source#gpu and https://developer.nvidia.com/tensorrt
tf_versions_map = {
    "1.15.3" : {
        "TENSORRT_REPO_FILE" : "nv-tensorrt-repo-ubuntu1804-cuda10.0-trt6.0.1.5-ga-20190913_1-1_amd64.deb",
        "TENSORRT_REPO_DOWNLOAD_URL" : "https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/6.0/GA_6.0.1.5/local_repos/nv-tensorrt-repo-ubuntu1804-cuda10.0-trt6.0.1.5-ga-20190913_1-1_amd64.deb",
        "TENSORRT_REPO_DOWNLOAD_URL" : "",
        "CUDA_VER_NUM" : "10.0",
        "CUDA_VER_MAJOR" : "10",
        "CUDA_VER_MINOR" : "0",
        "CUDA_VER_TEXT" : "cuda10.0",
        "CUDA_VER_DASH" : "10-0",
        "CUDNN_VER_FULL" : "7.6.3.30-1",
        "CUDNN_VER_MAJOR" : "7",
        "TRT_VER_FULL" : "6.0.1.5-1",
        "NVINFER_VER" : "6.0.1-1",
        "TRT_VER_MAJOR" : "6",
        "BAZEL_VER" : "0.26.1"
    },
    "2.0.0" : {
        "TENSORRT_REPO_FILE" : "nv-tensorrt-repo-ubuntu1804-cuda10.0-trt6.0.1.5-ga-20190913_1-1_amd64.deb",
        "TENSORRT_REPO_DOWNLOAD_URL" : "https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/6.0/GA_6.0.1.5/local_repos/nv-tensorrt-repo-ubuntu1804-cuda10.0-trt6.0.1.5-ga-20190913_1-1_amd64.deb",
        "TENSORRT_REPO_DOWNLOAD_URL" : "",
        "CUDA_VER_NUM" : "10.0",
        "CUDA_VER_MAJOR" : "10",
        "CUDA_VER_MINOR" : "0",
        "CUDA_VER_TEXT" : "cuda10.0",
        "CUDA_VER_DASH" : "10-0",
        "CUDNN_VER_FULL" : "7.6.3.30-1",
        "CUDNN_VER_MAJOR" : "7",
        "TRT_VER_FULL" : "6.0.1.5-1",
        "NVINFER_VER" : "6.0.1-1",
        "TRT_VER_MAJOR" : "6",
        "BAZEL_VER" : "0.26.1"
    },
    "2.3.0" : {
        "TENSORRT_REPO_FILE" : "nv-tensorrt-repo-ubuntu1804-cuda11.0-trt7.2.2.3-ga-20201211_1-1_amd64.deb",
        "TENSORRT_REPO_DOWNLOAD_URL" : "https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/7.2.2/local_repos/nv-tensorrt-repo-ubuntu1804-cuda11.0-trt7.2.2.3-ga-20201211_1-1_amd64.deb",
        "CUDA_VER_NUM" : "11.0",
        "CUDA_VER_MAJOR" : "11",
        "CUDA_VER_MINOR" : "0",
        "CUDA_VER_TEXT" : "cuda11.0",
        "CUDA_VER_DASH" : "11-0",
        "CUDNN_VER_FULL" : "8.0.5.39-1",
        "CUDNN_VER_MAJOR" : "8",
        "TRT_VER_FULL" : "7.2.1.6-1",
        "NVINFER_VER" : "7.2.1-1",
        "TRT_VER_MAJOR" : "7",
        "BAZEL_VER" : "3.1.0"
    },
    "2.4.0" : {
        "TENSORRT_REPO_FILE" : "nv-tensorrt-repo-ubuntu1804-cuda11.0-trt7.2.2.3-ga-20201211_1-1_amd64.deb",
        "TENSORRT_REPO_DOWNLOAD_URL" : "https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/7.2.2/local_repos/nv-tensorrt-repo-ubuntu1804-cuda11.0-trt7.2.2.3-ga-20201211_1-1_amd64.deb",
        "CUDA_VER_NUM" : "11.0",
        "CUDA_VER_MAJOR" : "11",
        "CUDA_VER_MINOR" : "0",
        "CUDA_VER_TEXT" : "cuda11.0",
        "CUDA_VER_DASH" : "11-0",
        "CUDNN_VER_FULL" : "8.0.5.39-1",
        "CUDNN_VER_MAJOR" : "8",
        "TRT_VER_FULL" : "7.2.2.3-1",
        "NVINFER_VER" : "7.2.2-1",
        "TRT_VER_MAJOR" : "7",
        "BAZEL_VER" : "3.1.0"
    }
}

bash_script_file_in = Path(__file__).parent.absolute() / "install_prerequisites.sh.in"
bash_script_file_out = "/tmp/install_prerequisites.sh"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tf-version")
    parser.add_argument("--local-repo-dir")
    args = parser.parse_args()

    with open(bash_script_file_in, 'r') as script_in, open(bash_script_file_out, 'w') as script_out:
        script_template = script_in.read()
        for key, value in tf_versions_map[args.tf_version].items():
            if key == "TENSORRT_REPO_FILE":
                script_template = script_template.replace("@" + key + "@", args.local_repo_dir + value)
            else:
                script_template = script_template.replace("@" + key + "@", value)
        script_template = script_template.replace("@ARCH@", arch)
        script_template = script_template.replace("@UBUNTU_VERSION_NAME@", ubuntu_version_name)
        script_template = script_template.replace("@UBUNTU_VERSION_NUMERIC@", ubuntu_version_numeric)
        script_out.write(script_template)

    chmod(bash_script_file_out, stat.S_IRWXU | stat.S_IRWXG)
