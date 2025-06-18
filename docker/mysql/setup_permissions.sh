#!/bin/bash
set -e

echo " Waiting for MySQL to be ready..."
until mysqladmin ping --silent; do
  sleep 1
done
echo " MySQL ready..."

mysql -uroot -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
  GRANT ALL PRIVILEGES ON \`test_%\`.* TO 'rrh'@'%';
  FLUSH PRIVILEGES;
EOSQL