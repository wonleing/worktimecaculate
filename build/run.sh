#!/bin/bash
/sbin/a2enmod wsgi
apache2ctl -k start
tail -f /var/log/apache2/error.log
