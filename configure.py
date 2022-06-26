#!/bin/python

import argparse
import os
from pathlib import Path
import stat

arch = "x86_64"
# arch = "arm64"

ubuntu_version_name = "focal"
ubuntu_version_numeric = "2004"
ubuntu_version_dot = "20.04"
# ubuntu_version_name = "bionic"
# ubuntu_version_numeric = "1804"
# ubuntu_version_dot = "18.04"

# https://developer.nvidia.com/tensorrt
# https://developer.nvidia.com/nvidia-tensorrt-8x-download

# Versions taken from https://www.tensorflow.org/install/source#gpu_support_3 and https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorflow
# Detailed Frameworks Support Matrix by Nvidia - https://docs.nvidia.com/deeplearning/frameworks/support-matrix/
tf_versions_map = {
    "1.15.3" : {
        "TENSORRT_REPO_FILE" : "nv-tensorrt-repo-ubuntu1804-cuda10.0-trt6.0.1.5-ga-20190913_1-1_amd64.deb",
        "TENSORRT_REPO_NAME" : "nv-tensorrt-repo-ubuntu1804-cuda10.0-trt6.0.1.5-ga-20190913",
        "TENSORRT_REPO_DOWNLOAD_URL" : "https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/6.0/GA_6.0.1.5/local_repos/nv-tensorrt-repo-ubuntu1804-cuda10.0-trt6.0.1.5-ga-20190913_1-1_amd64.deb",
        "CUDA_VER_NUM" : "10.0",
        "CUDA_VER_MAJOR" : "10",
        "CUDA_VER_MINOR" : "0",
        "CUDA_VER_TEXT" : "cuda10.0",
        "CUDA_VER_DASH" : "10-0",
        "TRT_VER_FULL" : "6.0.1.5-1",
        "NVINFER_VER" : "6.0.1-1",
        "TRT_VER_MAJOR" : "6",
        "BAZEL_VERSION" : "0.26.1"
    },
    "2.0.0" : {
        "TENSORRT_REPO_FILE" : "nv-tensorrt-repo-ubuntu1804-cuda10.0-trt6.0.1.5-ga-20190913_1-1_amd64.deb",
        "TENSORRT_REPO_NAME" : "nv-tensorrt-repo-ubuntu1804-cuda10.0-trt6.0.1.5-ga-20190913",
        "TENSORRT_REPO_DOWNLOAD_URL" : "https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/6.0/GA_6.0.1.5/local_repos/nv-tensorrt-repo-ubuntu1804-cuda10.0-trt6.0.1.5-ga-20190913_1-1_amd64.deb",
        "CUDA_VER_NUM" : "10.0",
        "CUDA_VER_MAJOR" : "10",
        "CUDA_VER_MINOR" : "0",
        "CUDA_VER_TEXT" : "cuda10.0",
        "CUDA_VER_DASH" : "10-0",
        "TRT_VER_FULL" : "6.0.1.5-1",
        "NVINFER_VER" : "6.0.1-1",
        "TRT_VER_MAJOR" : "6",
        "BAZEL_VERSION" : "0.26.1"
    },
    "2.3.0" : {
        "TENSORRT_REPO_FILE" : "nv-tensorrt-repo-ubuntu1804-cuda11.0-trt7.2.2.3-ga-20201211_1-1_amd64.deb",
        "TENSORRT_REPO_NAME" : "nv-tensorrt-repo-ubuntu1804-cuda11.0-trt7.2.2.3-ga-20201211",
        "TENSORRT_REPO_DOWNLOAD_URL" : "https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/7.2.2/local_repos/nv-tensorrt-repo-ubuntu1804-cuda11.0-trt7.2.2.3-ga-20201211_1-1_amd64.deb",
        "CUDA_VER_NUM" : "11.0",
        "CUDA_VER_MAJOR" : "11",
        "CUDA_VER_MINOR" : "0",
        "CUDA_VER_TEXT" : "cuda11.0",
        "CUDA_VER_DASH" : "11-0",
        "TRT_VER_FULL" : "7.2.2.3-1",
        "NVINFER_VER" : "7.2.2-1",
        "TRT_VER_MAJOR" : "7",
        "BAZEL_VERSION" : "3.1.0"
    },
    "2.4.0" : {
        "TENSORRT_REPO_FILE" : "nv-tensorrt-repo-ubuntu1804-cuda11.0-trt7.2.2.3-ga-20201211_1-1_amd64.deb",
        "TENSORRT_REPO_NAME" : "nv-tensorrt-repo-ubuntu1804-cuda11.0-trt7.2.2.3-ga-20201211",
        "TENSORRT_REPO_DOWNLOAD_URL" : "https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/7.2.2/local_repos/nv-tensorrt-repo-ubuntu1804-cuda11.0-trt7.2.2.3-ga-20201211_1-1_amd64.deb",
        "CUDA_VER_NUM" : "11.0",
        "CUDA_VER_MAJOR" : "11",
        "CUDA_VER_MINOR" : "0",
        "CUDA_VER_TEXT" : "cuda11.0",
        "CUDA_VER_DASH" : "11-0",
        "TRT_VER_FULL" : "7.2.2.3-1",
        "NVINFER_VER" : "7.2.2-1",
        "TRT_VER_MAJOR" : "7",
        "BAZEL_VERSION" : "3.1.0"
    },
    "2.9.0" : {
        "TENSORRT_REPO_FILE" : "nv-tensorrt-repo-ubuntu2004-cuda11.6-trt8.4.1.5-ga-20220604_1-1_amd64.deb",
        "TENSORRT_REPO_NAME" : "nv-tensorrt-repo-ubuntu2004-cuda11.6-trt8.4.1.5-ga-20220604",
        "TENSORRT_REPO_DOWNLOAD_URL" : "https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/8.4.1/local_repos/nv-tensorrt-repo-ubuntu2004-cuda11.6-trt8.4.1.5-ga-20220604_1-1_amd64.deb",
        "CUDA_VER_NUM" : "11.6",
        "CUDA_VER_MAJOR" : "11",
        "CUDA_VER_MINOR" : "6",
        "CUDA_VER_TEXT" : "cuda11.6",
        "CUDA_VER_DASH" : "11-6",
        "TRT_VER_FULL" : "8.4.1.5-1",
        "NVINFER_VER" : "8.4.1-1",
        "TRT_VER_MAJOR" : "8",
        "BAZEL_VERSION" : "5.0.0"
    }
}

bash_script_files = [
    Path(__file__).parent.absolute() / "install_prerequisites.sh.in",
    Path(__file__).parent.absolute() / "install_bazel.sh.in"
]

output_directory = Path("./output")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tf-version")
    parser.add_argument("--local-repo-dir")
    parser.add_argument("--output-dir")
    args = parser.parse_args()

    if args.output_dir:
        output_directory = Path(args.output_dir)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for bash_script_file_in in bash_script_files:
        bash_script_file_out = output_directory / str(bash_script_file_in.name)[0 : -3]
        with open(bash_script_file_in, 'r') as script_in, open(bash_script_file_out, 'w') as script_out:
            script_template = script_in.read()
            for key, value in tf_versions_map[args.tf_version].items():
                if key == "TENSORRT_REPO_FILE":
                    script_template = script_template.replace("@" + key + "@", str(Path(args.local_repo_dir) / value))
                else:
                    script_template = script_template.replace("@" + key + "@", value)
            script_template = script_template.replace("@ARCH@", arch)
            script_template = script_template.replace("@UBUNTU_VERSION_NAME@", ubuntu_version_name)
            script_template = script_template.replace("@UBUNTU_VERSION_NUMERIC@", ubuntu_version_numeric)
            script_out.write(script_template)
        os.chmod(bash_script_file_out, stat.S_IRWXU | stat.S_IRWXG)

