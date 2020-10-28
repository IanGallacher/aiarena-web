FROM python:3.7-slim

RUN apt-get update -qq && apt-get install -y build-essential

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# needed for webpacker
RUN apt-get install -y nodejs npm

# Setup MySQL
RUN apt-get install -y apt-utils lsb-release wget \
 && echo "mysql-apt-config mysql-apt-config/select-product select Apply" | debconf-set-selections \
 && echo "mysql-apt-config mysql-apt-config/select-server select mysql-5.7" | debconf-set-selections \
 && wget https://dev.mysql.com/get/mysql-apt-config_0.8.13-1_all.deb \
 && dpkg -i ./mysql-apt-config_0.8.13-1_all.deb \
 && apt-get update \
 && apt-get install -y mysql-server mysql-community-server mysql-client mysql-community-client libmysqlclient-dev

# Git is required for pip intall
RUN apt-get install -y git

# Setup the virtual path that will be used for building the image.
ENV APP_HOME /aiarena-web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# If a COPY file changes, then docker will rebuild from that step onwards.
# We only want to rerun `pip install` if the requirements file changes, not if
# any file in the project changes.
# For now, let's only COPY the requirements files, the other files can be added
# later.
COPY ./pip/requirements.txt $APP_HOME/pip/
COPY ./pip/requirements.DEVELOPMENT.txt $APP_HOME/pip/
RUN pip install -r ./pip/requirements.txt
RUN pip install -r ./pip/requirements.DEVELOPMENT.txt

# Again, only COPY the django-discord-bind repo, as it only needs to be rebuilt
# if any of its files change.
COPY ./django-discord-bind $APP_HOME/django-discord-bind/
RUN python ./django-discord-bind/setup.py install --force

# Finally, add the rest of the project into the image.
COPY . $APP_HOME
