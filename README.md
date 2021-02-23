# Worktimecaculate
work time caculate, powered by django

# How to run
run as dev: python manage.py runserver <IP>:8000
run with wsgi: To be added
run in container: To be added

# DB setting and init
recommend to use mysql/mariadb
1. `sudo apt-get install default-mysql-server mysql python-mysqldb`
2. set root password as 'deepin', plugin as 'mysql_native_password' following https://www.cnblogs.com/cpl9412290130/p/9583868.html
3. login mysql with 'mysql -uroot -p', input password and create DB 'beiyan' with: `CREATE DATABASE IF NOT EXISTS beiyan DEFAULT CHARSET utf8 COLLATE utf8_general_ci;`
4. `rm gstj/migrations/000*;python manage.py makemigrations`
5. `python manage.py migrate`
6. `python manage.py createsuperuser`, set admin password as 'deepin123'
7. `python loaddata db_data.json`
