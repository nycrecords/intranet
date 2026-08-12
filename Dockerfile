# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-PYTHON_VERSION_NOT_SET}

FROM python:${INSTALL_PYTHON_VERSION}-slim-bullseye AS builder

RUN apt-get update
RUN apt-get -y install pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl gcc

WORKDIR /app

# See https://github.com/moby/moby/issues/37965
RUN true
COPY requirements requirements
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache -r requirements/prod.txt

COPY intranet.py ./
COPY app app
COPY .env.example .env

# ================================= PRODUCTION =================================
FROM python:${INSTALL_PYTHON_VERSION}-slim-buster as production

RUN apt-get update
RUN apt-get -y install pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl gcc

WORKDIR /app

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid
ENV PATH="/home/sid/.local/bin:${PATH}"

COPY --from=builder --chown=sid:sid /app/app/static /app/app/static
COPY requirements requirements
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache --user -r requirements/prod.txt

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisord_programs /etc/supervisor/conf.d

COPY . .

EXPOSE 5000
ENTRYPOINT ["/bin/bash", "shell_scripts/supervisord_entrypoint.sh"]
CMD ["-c", "/etc/supervisor/supervisord.conf"]


# ================================= DEVELOPMENT ================================
FROM builder AS development
RUN pip install --no-cache -r requirements/dev.txt
EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0" ]
