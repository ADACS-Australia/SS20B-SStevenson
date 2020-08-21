FROM nginx:1.19
COPY nginx/nginx.conf /etc/nginx/templates/default.conf.template
