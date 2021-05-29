FROM nginx:1.21.0

ARG NGINX_CONFIG_DIRECTORY=/etc/nginx/templates

COPY ["default.conf.template","$NGINX_CONFIG_DIRECTORY/"]