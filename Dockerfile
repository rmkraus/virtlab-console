FROM docker.io/library/fedora:31

# Install dependencies
RUN useradd www && \
    dnf update -y && \
    dnf install -y libyaml && \
    dnf install -y gcc && \
    python3 -m venv /opt/my_python && \
    /opt/my_python/bin/python -m pip install --upgrade pip && \
    /opt/my_python/bin/python -m pip install flask pyyaml && \
    dnf history undo last -y
WORKDIR /app
COPY app /app

# Setup startup environment
USER www
CMD /app/bin/entry.sh
