#!/bin/sh

# Navigate to the app directory
cd /app

# Download and unpack Mitmproxy
curl -sSL https://snapshots.mitmproxy.org/5.2/mitmproxy-5.2-linux.tar.gz | tar xvz

# Move mitmproxy to bin folder
mv mitmproxy /app/.heroku/python/bin/

# Copy the script to the bin folder
cp mitm_script.py /app/.heroku/python/bin/
