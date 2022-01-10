#!/bin/sh

# add kopf command to PATH
export PATH="$PATH:/home/webapp/.local/bin/"

# copy ca cert into ca trust
if test -f "$VENAFI_CA_CERT"; then
    cp $VENAFI_CA_CERT /usr/local/share/ca-certificates;
    update-ca-certificates;
else
    echo "Could not find local cert "$VENAFI_CA_CERT", skipping copy";
fi

# export ca cert requests should use
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# run the operator
kopf run -A --standalone --liveness=http://0.0.0.0:8080/healthz /app/src/main.py $KOPF_EXTRA_ARGS