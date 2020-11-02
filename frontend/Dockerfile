FROM node:14.15-alpine as build
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY package*.json /usr/src/app/
RUN npm install
COPY . /usr/src/app/
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]

FROM nginx:stable
COPY --from=build /usr/src/app/build /usr/share/nginx/html
COPY --from=build /usr/src/app/certs /etc/nginx/certs
# COPY ./nginx.template /etc/nginx/nginx.template
COPY ./nginx.template /etc/nginx/conf.d/default.conf.template
COPY ./nginx.conf /etc/nginx/nginx/conf
# CMD ["nginx", "-g", "daemon off;"]
# CMD ["/bin/sh", "-c", "envsubst < /etc/nginx/nginx.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
CMD /bin/bash -c "envsubst '\$PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf" && nginx -g 'daemon off;'