FROM python:3.10-slim-bullseye

# setup app directory with code/user
WORKDIR /app
RUN adduser -u 1000 webapp -q && chown webapp:webapp /app
COPY --chown=webapp:webapp . /app
RUN chown -R webapp /etc/ssl/certs && chown -R webapp /usr/local/share/ca-certificates

# environment variables to set
ENV KOPF_EXTRA_ARGS "--verbose"
ENV VENAFI_CA_CERT "/app/ssl/tls.crt"
ENV VENAFI_DNS_DOMAIN ""
ENV VENAFI_AUTH_TOKEN ""

# run as non-root user
USER webapp

# get required dependencies
RUN pip3 install -r /app/requirements.txt

# run lint checks
RUN python3 -m pylint $(echo -n ./src/*.py && echo -n ' ' && find . -type d -maxdepth 1 -exec test -e '{}'/__init__.py \; -print | grep -v '^./\.') -j0

# start kopf
ENTRYPOINT [ "/app/run.sh" ]