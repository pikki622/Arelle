# Use oldest release with standard support for linked glibc compatibility
FROM ubuntu:18.04

ARG OPENSSL_VERSION
ARG PYTHON_VERSION
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get dist-upgrade -y && \
    apt-get install -y \
        build-essential \
        curl \
        git \
        libbz2-dev \
        libffi-dev \
        libgdbm-compat-dev \
        libgdbm-dev \
        liblzma-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libnss3-dev \
        libreadline-dev \
        libsqlite3-dev \
        libtk8.6 \
        libxml2-dev \
        libxmlsec1-dev \
        llvm \
        make \
        tk-dev \
        unixodbc-dev \
        uuid-dev \
        wget \
        xz-utils \
        zlib1g-dev

WORKDIR /tmp

RUN wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz \
    && tar xzf openssl-${OPENSSL_VERSION}.tar.gz \
    && (cd openssl-${OPENSSL_VERSION} \
        && ./config \
            -fPIC \
            --openssldir=/usr/local/ssl \
            --prefix=/usr/local \
            no-shared \
            no-ssl2 \
        && make \
        && make install --jobs "$(nproc)") \
    && rm -r ./openssl-${OPENSSL_VERSION} \
    && rm ./openssl-${OPENSSL_VERSION}.tar.gz

RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
    && tar xzf Python-${PYTHON_VERSION}.tgz \
    && (cd Python-${PYTHON_VERSION} \
        && ./configure \
            --enable-optimizations \
            --enable-shared \
            --with-computed-gotos \
            --with-lto \
            --with-openssl=/usr/local \
            --with-system-ffi \
        && make install --jobs "$(nproc)") \
    && rm -r ./Python-${PYTHON_VERSION} \
    && rm ./Python-${PYTHON_VERSION}.tgz

RUN pip3 install --upgrade pip setuptools wheel

WORKDIR /build

ADD ../requirements*.txt .

RUN pip3 install -r requirements-build.txt

ADD ../ /build

RUN /bin/sh ./scripts/buildLinuxDist.sh ubuntu

ENTRYPOINT ["/bin/sh", "-c"]
