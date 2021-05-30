FROM nginx:1.21.0

COPY ["default.conf.template","/etc/nginx/templates/"]
COPY ["nginx_validator.js", "/etc/nginx/conf.d/"]
COPY ["nginx.conf", "/etc/nginx/"]