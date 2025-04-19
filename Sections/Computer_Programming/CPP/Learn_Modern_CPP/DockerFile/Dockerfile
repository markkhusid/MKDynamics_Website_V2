# Use Ubuntu 24.04 as the base image
FROM ubuntu:24.04 AS build

# Update package lists and install necessary tools
RUN apt update && apt install -y \
    wget \
    gnupg \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Add the LLVM repository for Clang 18
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - \
    && echo "deb http://apt.llvm.org/noble/ llvm-toolchain-noble-18 main" >> /etc/apt/sources.list \
    && apt update

# Install Clang 18
RUN apt install -y clang-18 lld-18 libc++-18-dev libc++abi-18-dev

# Set Clang 18 as the default compiler
RUN update-alternatives --install /usr/bin/clang clang /usr/bin/clang-18 100 \
    && update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-18 100

# Set working directory
WORKDIR /app

# Copy your C++ source code into the container (optional)
COPY . .

# Start an interactive shell
CMD ["bash"]