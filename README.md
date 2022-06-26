# ML-utils
A personal collection of scripts and tools facilitating easier research and development of machine learning applications. Mostly intended for quickly setting-up Docker containers.

Setting up ARM based machines (embedded devices) is not yet supported, but is planned.


## Usage
***python3 configure.py --tf-version <1.15.3 | 2.3.0 | 2.4.0 | 2.9.0> --local-repo-dir \<path to the directory with the TensorRT's local repo .deb files\> --output-dir \<path to the directory to save the script\>***  

This creates two scripts - **install_bazel.sh** and **install_prerequisites**.sh, which install all packages needed for development with the specific version of TensorFlow using TensorRT for GPU acceleration.  
In addition **build_tensorflow_cpp.sh** can be used to create and install the C++ bindings of TensorFlow, which have to be build from source. They don't have official binary distribution, but are officially supported.

## Docker
[The NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
