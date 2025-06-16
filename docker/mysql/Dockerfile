ARG MYSQL_VERSION
FROM mysql:${MYSQL_VERSION}

ARG TZ=UTC
ENV TZ ${TZ}

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
 && echo $TZ > /etc/timezone \
 && chown -R mysql:root /var/lib/mysql/

COPY setup_permissions.sh /docker-entrypoint-initdb.d/setup_permissions.sh
RUN chmod +x /docker-entrypoint-initdb.d/setup_permissions.sh

EXPOSE 3306