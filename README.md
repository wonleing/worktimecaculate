# Worktimecaculate
work time caculate, powered by django

# How to run
## run as dev:
  python manage.py runserver <IP>:8000

## run with wsgi: 
  apt install libapache2-mod-wsgi apache2
  add similar config into /etc/apache2/apache2.conf, following https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
```shell
Alias /static/ /home/uos_server9_58_203/code/worktimecaculate/static/
<Directory /home/uos_server9_58_203/code/worktimecaculate/static>
  Options Indexes FollowSymLinks
  AllowOverride None
  Require all granted
</Directory>
<Directory /home/uos_server9_58_203/code/worktimecaculate/gstj>
  <Files wsgi.py>
    Require all granted
  </Files>
</Directory>
WSGIDaemonProcess gstj python-path=/home/uos_server9_58_203/code/worktimecaculate/
WSGIProcessGroup gstj
WSGIScriptAlias / /home/uos_server9_58_203/code/worktimecaculate/gstj/wsgi.py
```
## run in container: To be added
1. `git clone https://github.com/wonleing/worktimecaculate.git`  Pull source code.
2. `cd build`   Enter the code build directory
3. `sudo docker build . -t worktimecaculate:v1 -f Dockerfile` Use the Dockerfile in the code file to build the image
4. `sudo docker run -d -p 80:80 -v /opt/worktimecaculate/:/opt/worktimecaculate/ --name worktimecaculate -e MYSQL_HOST=<mariadb_ip> -e MYSQL_USER=root -e MYSQL_PASSWD=deepin  worktimecaculate:v1` Start the container
5. `cp -r * /opt/worktimecaculate `  Copy the source code to the directory
6.  Perform initialization

# DB setting and init
recommend to use mysql/mariadb
1. `sudo apt-get install default-mysql-server mycli python-mysqldb`
2. set root password as 'deepin', plugin as 'mysql_native_password' following https://www.cnblogs.com/cpl9412290130/p/9583868.html
3. login mysql with 'mysql -uroot -p', input password and create DB 'beiyan' with: `CREATE DATABASE IF NOT EXISTS beiyan DEFAULT CHARSET utf8 COLLATE utf8_general_ci;`
4. edit gstj/setting, change DB IP and username/password accordingly
5. `rm gstj/migrations/000*;python manage.py makemigrations gstj`
6. `python manage.py migrate`
7. `python manage.py createsuperuser`, set admin password as 'deepin123'
8. `python manage.py loaddata db_data.json`
