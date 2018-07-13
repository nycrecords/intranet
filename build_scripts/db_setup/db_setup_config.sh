#!/usr/bin/env bash
# 1. Create postgres users
sudo -u postgres /opt/rh/rh-postgresql95/root/usr/bin/createuser -s -e developer
sudo -u postgres /opt/rh/rh-postgresql95/root/usr/bin/createuser -s -e intranet_db

# 2. Create database
sudo -u postgres /opt/rh/rh-postgresql95/root/usr/bin/createdb intranet