FROM nginx:1.19
ENV DEBCONF_NOWARNINGS yes
ENV DEBIAN_FRONTEND noninteractive
RUN set -xe \
&& apt-get update -y \
&& apt-get install -y --no-install-recommends vim curl locales certbot \
&& apt-get clean -y \
&& rm -rf /var/lib/apt/lists/* \
&& locale-gen ja_JP.UTF-8 \
&& localedef -f UTF-8 -i ja_JP ja_JP.utf8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:jp
ENV LC_ALL ja_JP.UTF-8
ENV LC_CTYPE ja_JP.UTF-8
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]