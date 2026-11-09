FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive
ARG HADOOP_VERSION=3.3.6

# bullseye ya es EOL: sus repos están en archive.debian.org
RUN echo "deb http://archive.debian.org/debian bullseye main" > /etc/apt/sources.list \
    && echo "deb http://archive.debian.org/debian-security bullseye-security main" >> /etc/apt/sources.list \
    && echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99archive
    
# Java, Python, SSH y herramientas básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
        openjdk-11-jdk-headless python3 \
        openssh-server openssh-client \
        curl ca-certificates procps \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Descargar e instalar Hadoop (modo standalone)
RUN curl -fsSL https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
        | tar -xz -C /opt \
    && mv /opt/hadoop-${HADOOP_VERSION} ${HADOOP_HOME}

# Usuario sin privilegios, sin contraseña (el '*' bloquea login por password, pero permite llaves)
RUN useradd -m -s /bin/bash hadoop \
    && usermod -p '*' hadoop \
    && mkdir -p /run/sshd /data/input /data/output \
    && echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh \
    && chown -R hadoop:hadoop /data ${HADOOP_HOME}

# Llaves SSH sin passphrase para el usuario hadoop
USER hadoop
RUN mkdir -p ~/.ssh \
    && ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519 \
    && cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys \
    && printf "Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n" > ~/.ssh/config \
    && chmod 700 ~/.ssh \
    && chmod 600 ~/.ssh/authorized_keys ~/.ssh/config ~/.ssh/id_ed25519 \
    && echo "export JAVA_HOME=${JAVA_HOME}" >> ~/.bashrc \
    && echo "export HADOOP_HOME=${HADOOP_HOME}" >> ~/.bashrc \
    && echo 'export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' >> ~/.bashrc

# sshd necesita root para arrancar
USER root
EXPOSE 22
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
