#!/bin/bash

APPNAME="tapease"
DBPW="pw4db"

echo "************************"
echo " INSTALLING tapease SERVER "
echo "************************"
echo "\n"

sudo yum update
sudo yum install mysql
sudo yum install mysql-server
sudo yum install httpd
sudo yum install git

echo "\n"
echo "*******************"
echo " CONFIGURING MYSQL "
echo "*******************"
echo "\n"

sudo service mysqld start
sudo /usr/bin/mysql_secure_installation

cat > ~/.my.cnf <<EOF
[client]
host = localhost
user = root
password = $DBPW
EOF
mysql -e "CREATE SCHEMA tapease"
mysql -e "CREATE USER 'web2py-tapease'@'localhost' IDENTIFIED BY 'pw4web2py';"
mysql -e "GRANT ALL ON tapease.* TO 'web2py-tapease'@'localhost';"
mysql -e "CREATE USER 'hnguyen'@'%' IDENTIFIED BY 'pw4amazondbhenry';"
mysql -e "GRANT ALL ON *.* TO 'hnguyen'@'%';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'hnguyen'@'%' WITH GRANT OPTION;"
mysql -e "FLUSH PRIVILEGES;"

echo "\n"
echo "*******************"
echo " INSTALLING WEB2PY "
echo "*******************"
echo "\n"

cd ~/
wget http://web2py.googlecode.com/hg/scripts/setup-web2py-fedora.sh
chmod 764 setup-web2py-fedora.sh
sudo ./setup-web2py-fedora.sh
sudo chown -R apache:ec2-user /opt/web-apps/web2py
sudo rm ~/web2py_src.zip

echo "\n"
echo "*********************"
echo " GENERATING SSH KEYS "
echo "*********************"
echo "\n"

cd ~/.ssh
ssh-keygen -t rsa
cat id_rsa.pub
/usr/bin/ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
ssh-add

echo "\n"
echo "**************"
echo " CLONING REPO "
echo "**************"
echo "\n"

cd /opt/web-apps/web2py/applications/
sudo git clone https://github.com/henrynguyen7/tapease-web2py.git tapease
sudo cp /opt/web-apps/web2py/applications/tapease/routes.py /opt/web-apps/web2py/
sudo mkdir /opt/web-apps/web2py/applications/tapease/cron/
sudo mkdir /opt/web-apps/web2py/applications/tapease/databases/
sudo mkdir /opt/web-apps/web2py/applications/tapease/errors/
sudo mkdir /opt/web-apps/web2py/applications/tapease/languages/
sudo mkdir /opt/web-apps/web2py/applications/tapease/modules/
sudo mkdir /opt/web-apps/web2py/applications/tapease/sessions/
sudo mkdir /opt/web-apps/web2py/applications/tapease/static/
sudo mkdir /opt/web-apps/web2py/applications/tapease/uploads/
sudo mkdir /opt/web-apps/web2py/applications/tapease/private/
cat > /opt/web-apps/web2py/applications/tapease/private/conf.json <<EOF
{
    "mysql": {
        "username": "web2py-tapease",
        "password": "pw4web2py",
        "database": "tapease",
        "host": "127.0.0.1",
        "port": "3306"
    }
}
EOF
sudo chown -R apache:ec2-user /opt/web-apps/web2py

echo "\n"
echo "****************************"
echo " CREATING GIT-DEPLOY SCRIPT "
echo "****************************"
echo "\n"

cat > ~/git-pull-tapease.sh <<EOF
#!/bin/bash
cd /opt/web-apps/web2py/applications/tapease
git reset --hard
git pull
sudo service httpd restart
EOF
sudo chmod 764 ~/git-pull-tapease.sh

echo "\n"
echo "*****************"
echo " STARTING SERVER "
echo "*****************"
echo "\n"

sudo service httpd restart

echo "\n"
echo "***********************"
echo " INSTALLATION COMPLETE "
echo "***********************"
echo "\n"
