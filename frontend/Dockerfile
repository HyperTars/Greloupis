FROM node:14.15-alpine as build
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ARG ACCESS_KEY_ID1
ARG ACCESS_KEY_ID2
ARG SECRET_KEY1
ARG SECRET_KEY2
ENV ACCESS_KEY_ID1=$ACCESS_KEY_ID1
ENV SECRET_KEY1=$SECRET_KEY1
ENV ACCESS_KEY_ID2=$ACCESS_KEY_ID2
ENV SECRET_KEY2=$SECRET_KEY2
COPY package*.json /usr/src/app/
RUN npm install
COPY . /usr/src/app/
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /usr/src/app/build /usr/share/nginx/html
COPY configs/nginx.template /etc/nginx/conf.d/default.conf.template
COPY configs/nginx.conf /etc/nginx/nginx/conf
CMD /bin/sh -c "envsubst '\$PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf" && nginx -g 'daemon off;'