FROM apache/superset:latest

USER root


RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

RUN pip install mysqlclient

RUN pip install pinotdb

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASWORD $ADMIN_PASSWORD

COPY ./superset-init.sh /superset-init.sh

RUN chmod +x /superset-init.sh

COPY superset_config.py /app/
ENV  SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]
