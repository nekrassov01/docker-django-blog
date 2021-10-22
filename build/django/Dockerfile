FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8 
ENV DEBCONF_NOWARNINGS yes
ENV DEBIAN_FRONTEND noninteractive
ARG DIR=/django
RUN mkdir -p $DIR
WORKDIR $DIR
COPY requirements.txt $DIR/
RUN set -ex \
&& apt-get update -y \
&& apt-get install -y --no-install-recommends vim git curl locales postgresql-client \
&& apt-get clean -y \
&& rm -rf /var/lib/apt/lists/* \
&& locale-gen ja_JP.UTF-8 \
&& localedef -f UTF-8 -i ja_JP ja_JP.utf8 \
&& pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:jp
ENV LC_ALL ja_JP.UTF-8
ENV LC_CTYPE ja_JP.UTF-8
CMD ["uwsgi","--ini","/django/uwsgi.ini"]