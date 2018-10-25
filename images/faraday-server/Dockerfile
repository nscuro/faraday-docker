FROM ubuntu:18.04

# Database environment variables
ENV POSTGRES_USER change-me
ENV POSTGRES_PASSWORD change-me
ENV POSTGRES_DB change-me
ENV POSTGRES_HOST change-me

# Faraday environment variables
ENV FARADAY_SUPERUSER_NAME faraday
ENV FARADAY_SUPERUSER_EMAIL faraday@faradaysec.com
ENV FARADAY_SUPERUSER_PASSWORD faraday

# Install required tools for faraday download
RUN apt update && apt install -y git

# Close faraday git repository
WORKDIR /root
RUN git clone https://github.com/infobyte/faraday.git

# Checkout a stable release version
WORKDIR /root/faraday
RUN git checkout tags/v3.1.1 -b v3.1.1

# Install the server's system dependencies
RUN apt install -y  python build-essential ipython \
    python-setuptools python-pip python-dev \
    libssl-dev libffi-dev pkg-config libssl-dev \
    libffi-dev libxml2-dev libxslt1-dev libfreetype6-dev \
    libpng-dev libpq-dev

# Install the server's python dependencies
RUN pip install -U -r requirements_server.txt

# Temporary fix for incompatible dependency
RUN pip install --force-reinstall itsdangerous==0.24

# Apply default configuration files
RUN mkdir -p /root/.faraday/config && \
    cp /root/faraday/config/default.xml /root/.faraday/config/config.xml && \
    cp /root/faraday/server/default.ini /root/.faraday/config/server.ini

COPY ./run-faraday-server.py /root/run-faraday-server.py

CMD python /root/run-faraday-server.py \
    --faraday-root /root/faraday \
    --faraday-data /root/.faraday \
    --pg-user $POSTGRES_USER \
    --pg-pass $POSTGRES_PASSWORD \
    --pg-db $POSTGRES_DB \
    --pg-host $POSTGRES_HOST \
    --su-mail $FARADAY_SUPERUSER_EMAIL \
    --su-name $FARADAY_SUPERUSER_NAME \
    --su-pass $FARADAY_SUPERUSER_PASSWORD
