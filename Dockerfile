FROM docker.io/library/fedora:31

# Install dependencies
WORKDIR /app
COPY app /app
RUN useradd www && \
    dnf update -y && \
    dnf install -y libyaml nginx && \
    dnf install -y gcc && \
    python3 -m venv /opt/my_python && \
    /opt/my_python/bin/python -m pip install --upgrade pip && \
    /opt/my_python/bin/python -m pip install -r /app/requirements.txt && \
    dnf history undo last -y

# Install MongoDB
RUN echo -e '[Mongodb]\nname=MongoDB Repository\nbaseurl=https://repo.mongodb.org/yum/amazon/2/mongodb-org/4.2/x86_64/\ngpgcheck=1\nenabled=1\ngpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc' > /etc/yum.repos.d/mongodb.repo && \
    dnf install -y mongodb-org

# Setup startup environment
USER www
CMD /app/bin/entry.sh
