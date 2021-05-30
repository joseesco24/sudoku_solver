FROM nginx:1.21.0

COPY ["default.conf.template","/etc/nginx/templates/"]
COPY ["nginx.conf", "/etc/nginx/"]