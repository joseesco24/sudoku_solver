FROM nginx:1.21.0

ARG NGINX_CONFIG_DIRECTORY=/usr/local/nginx/conf
ARG USERNAME=production

RUN mkdir -p $NGINX_CONFIG_DIRECTORY
RUN useradd -ms /bin/bash $USERNAME

COPY ["nginx.conf","$NGINX_CONFIG_DIRECTORY/"]

USER $USERNAME