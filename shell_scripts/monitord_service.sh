#!/usr/bin/env bash

export FLASK_APP=intranet.py
export OPENSSL_CONF=/Users/vzheng/Desktop/intranet/openssl.cnf

cd /Users/vzheng/Desktop/intranet && /Users/vzheng/.local/share/virtualenvs/intranet-to7Wxv0y/bin/flask ping
