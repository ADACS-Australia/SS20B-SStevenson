FROM nginx:1.17.8
COPY docker/nginx-entrypoint.sh /nginx-entrypoint.sh
COPY src/nginx/nginx.conf /etc/nginx/config.template
RUN ["chmod", "+x", "/nginx-entrypoint.sh"]A
#CMD ["nginx", "-g", "daemon off;"]
#/etc/nginx/conf.d/default.conf
