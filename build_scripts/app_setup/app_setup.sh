#!/usr/bin/env bash

# 1. Install Python 3.5
yum -y install rh-python35

# 2. Install Redis 3.2
yum -y install rh-redis32

# 3. Setup /etc/profile.d/python.sh
bash -c "printf '#\!/bin/bash\nsource /opt/rh/rh-python35/enable\n' > /etc/profile.d/python35.sh"

# 4. Install Postgres Python Package (psycopg2) and Postgres Developer Package
yum -y install rh-postgresql95-postgresql-devel
yum -y install rh-python35-python-psycopg2
yum -y install openssl-devel
yum -y install libffi-devel
yum -y install libxml2-devel
yum -y install xmlsec1-devel
yum -y install xmlsec1-openssl-devel
yum -y install libtool-ltdl-devel

# 5. Setup SAML
mkdir -p /vagrant/saml
openssl req \
       -newkey rsa:4096 -nodes -keyout /vagrant/saml/saml.key \
       -x509 -days 365 -out /vagrant/saml/saml.crt -subj "/C=US/ST=New York/L=New York/O=NYC Department of Records and Information Services/OU=IT/CN=saml.intranet.dev"
openssl x509 -in /vagrant/saml/saml.crt -out /vagrant/saml/saml.pem -outform PEM

# 6. Install Developer Tools
yum -y groupinstall "Development Tools"

# 7. Install Required pip Packages
source /opt/rh/rh-python35/enable
pip install virtualenv
mkdir /home/vagrant/.virtualenvs
virtualenv --system-site-packages /home/vagrant/.virtualenvs/intranet
chown -R vagrant:vagrant /home/vagrant
source /home/vagrant/.virtualenvs/intranet/bin/activate
pip install -r /vagrant/requirements.txt --no-binary :all:

# 8. Install telnet-server
yum -y install telnet-server

# 9. Install telnet
yum -y install telnet

# 10. Automatically Use Virtualenv
echo "source /home/vagrant/.virtualenvs/intranet/bin/activate" >> /home/vagrant/.bash_profile

# 11. Add the following lines to /etc/sudoers file
#intranet   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis start
#intranet   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis stop
#intranet   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis status
#intranet   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis restart
#intranet   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis condrestart
#intranet   ALL=(ALL) NOPASSWD: /etc/init.d/rh-redis32-redis try-restart
