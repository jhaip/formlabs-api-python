# This is a multi-stage Dockerfile
# - 'headless_env' puts together the environment for PreForm Server
#   - note that running setup-xvfb.sh leaves the /tmp/.X99-lock file that would prevent running setup-xvfb.sh again (when the runner is invoked in production).
#   - by having its own stage, it won't affect the final image
# - 'final' is the final image with the entry point set to run the runner
#
# Note the '--platform=linux/amd64' parameters. Since PreForm Server is targeting this architecture,
# we force Dockerfile to build for that no matter what would be docker's default choice (e.g. arm64 on apple silicon)

#--- headless_env ---------------------------------------------
FROM --platform=linux/amd64 ubuntu:22.04 as headless_env
RUN mkdir -p /workspace
WORKDIR /workspace

ARG ZIP_PATH

RUN export DEBIAN_FRONTEND=noninteractive && \
  apt-get -y update && \
  apt-get -y --no-install-recommends install ca-certificates libfreetype6-dev libjpeg-dev libpng-dev \
  libpq-dev libcurl4-openssl-dev libssl-dev fontconfig \
  python3 python3-dev python3-pip && \
  apt-get -y install xvfb x11-utils && \
  apt-get -y install curl unzip wget && \
  rm -rf /var/lib/apt/lists/*

# --- Pre-built PreForm Server ---

RUN mkdir -p /workspace/preform/latest

COPY $ZIP_PATH /tmp/file.zip

RUN cd preform && \
  unzip -d latest /tmp/file.zip && \
  rm -rf /tmp/file.zip

# PreFormServer needs OpenSSL 1.1.1
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb && dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb  && rm libssl1.1_1.1.1f-1ubuntu2_amd64.deb # buildkit

ADD setup-xvfb.sh .
RUN chmod +x setup-xvfb.sh

ADD entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV DISPLAY=:99

#--- final ----------------------------------------------------
FROM headless_env as final

### Python app setup

ENV APP_HOME /workspace
ENV PYTHONUNBUFFERED TRUE

COPY . .

# Install production dependencies.
# RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
RUN chmod +x setup-xvfb.sh
ENTRYPOINT ["/workspace/entrypoint.sh"]
